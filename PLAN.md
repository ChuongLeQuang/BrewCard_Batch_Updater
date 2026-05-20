# KẾ HOẠCH DỰ ÁN: TRÌNH CẬP NHẬT SỐ LIỆU MẺ NẤU BREWCARD

## 🎯 1. Mục tiêu dự án
- Xây dựng phần mềm Desktop tự động hóa việc tổng hợp dữ liệu mẻ nấu (BrewCard) từ các tệp Excel con vào tệp Excel tổng.
- Đảm bảo tốc độ xử lý nhanh, bảo toàn 100% định dạng dữ liệu gốc (không dùng Pandas), chống treo ứng dụng (Not Responding) thông qua giao diện PyQt6 đa luồng.
- Cung cấp trải nghiệm người dùng (UX) hiện đại, trực quan với Dark Mode, chọn tọa độ ô bằng click chuột, kéo thả tệp và kiểm tra chất lượng (QC) tự động.

---

## 🧠 2. Giai đoạn 1: Thiết kế (Phase 1 - Design)

### 2.1. Luồng dữ liệu (Data Flow)
1. **Cấu hình (Config)**: Người dùng nhập thông số, click chọn tọa độ ô mẫu -> Dữ liệu lưu vào `data/configuration.json`.
2. **Tiếp nhận (Input)**: Kéo thả các tệp Excel cần tổng hợp vào hệ thống.
3. **Kiểm tra (QC)**: `QThread` đọc ngầm từng file qua OpenPyXL -> Đối chiếu JSON config -> Trả về danh sách Lỗi (Màu đỏ) / Đạt.
   - **Lưu vết (Logging)**: Tự động ghi nhận và cho phép trích xuất danh sách các dòng bị lỗi ra tệp `.txt` có gắn ngày giờ (VD: `logs/qc_errors_YYYYMMDD_HHMMSS.txt`).
4. **Tổng hợp (Sync)**:
   - Lọc các tệp Đạt.
   - Trích xuất dữ liệu từ file con: Đọc tọa độ tĩnh (VD: `C3`) hoặc phân dịch, tính toán công thức (VD: `L15 / E10 * 100`, hàm `IF`).
   - Đọc tệp Đích (BrewSync) vào RAM.
   - Đối chiếu **Số lô sản xuất (Batch Number)**:
     + Trùng: Cập nhật (Ghi đè dòng).
     + Mới: Chèn mới (Thêm vào cuối).
   - Sắp xếp tăng dần theo Số lô.
   - Ghi (Save) xuống tệp Đích duy nhất một lần.

### 2.2. Cấu trúc lưu trữ (Database / JSON Config)
**Tệp:** Quản lý đa cấu hình (Profiles) tại `data/profiles/<tên_profile>.json` (Lưu vết tại `data/app_settings.json`).
```json
{
    "target_file": {"path": "C:/...", "sheet_name": "BrewSync"},
    "input_file": {"sheet_name": "Sheet1"},
    "input_filter": {"type": "keyword", "value": "Brew"},
    "header_row": 5,
    "fingerprint": "D3=Order: & G3=Batch: & I3=Date:",
    "fallback_profile": "BrewCard_Old",
    "mappings": [
        {"target_col": "Batch Number", "target_col_letter": "B", "source_mapping": "H3"},
        {"target_col": "Mash-In Time", "target_col_letter": "G", "source_mapping": "IF(F19 >= F13, ...)"}
    ]
}
```

### 2.3. Các kịch bản ngoại lệ (Edge Cases & Error Handling)
- **Tệp bị khóa (Locked File)**: Đang mở trên Excel của Windows -> Bắt lỗi `PermissionError`, báo đỏ yêu cầu đóng file.
- **Dữ liệu rác/Trống (Null/Dirty Data)**: Lọc bỏ dòng trống, trim khoảng trắng; Báo cáo QC: `Sai - Trống dữ liệu`.
- **Sai công thức động**: `[C] / [D]` nhưng [D] = 0 -> Bắt lỗi `ZeroDivisionError`, trả về 0 hoặc báo lỗi.
- **Hiệu năng UI**: Render hàng ngàn dòng trong bảng QC -> Tắt cập nhật UI tạm thời (`setUpdatesEnabled(False)`), nạp dữ liệu, bật lại.
- **Tệp đích (BrewSync) không tồn tại**: Nếu file tổng chưa có, phần mềm tự động tạo file mới (kèm dòng tiêu đề) hoặc đưa ra cảnh báo yêu cầu người dùng chỉ định đường dẫn hợp lệ.

### 2.4. Quy định Ngữ pháp Công thức (Formula Grammar)
Bộ phân dịch `ExcelFormulaEvaluator` sẽ tuân thủ các quy tắc sau:

| Hạng mục | Quy tắc | Ví dụ Hợp lệ | Ví dụ KHÔNG Hợp lệ |
| :--- | :--- | :--- | :--- |
| **Tọa độ Ô** | Chỉ gồm chữ cái và số. | `A1`, `BC100` | `1A`, `A 1` |
| **Toán tử** | Hỗ trợ `+`, `-`, `*`, `/`, `^` (Lũy thừa), `&` (Nối chuỗi). | `A1+B2`, `A1^2`, `A1&B1` | - |
| **Số** | Hỗ trợ số nguyên và số thập phân. | `100`, `2.5`, `0.5` | `1,000` (Dấu phẩy) |
| **Khoảng trắng** | **Hoàn toàn bỏ qua**. | `A1*10` và `A1 * 10` là như nhau. | - |
| **Chữ hoa/thường**| **Hoàn toàn bỏ qua**. | `if(...)` và `IF(...)` là như nhau. | - |
| **Hàm `IF`** | Cú pháp: `IF(Điều kiện, Giá trị đúng, Giá trị sai)`. (Đánh giá lười - Lazy Evaluation) | `IF(A1>B2, 10, 20)` | `IF A1>B2 THEN 10` |
| **Các hàm Toán / Thống kê** | `SUM`, `AVERAGE`, `MIN`, `MAX`, `ABS`, `ROUND`, `COUNT`, `INT`, `MOD`. Chấp nhận dải ô (`A1:A5`) và liệt kê (`A1, B2`). | `SUM(A1:B10, C5)`, `MOD(A1, 2)` | `SUM A1:B10` |
| **Các hàm Logic khác** | `AND`, `OR`, `NOT`. Dùng để ghép nhiều điều kiện trong hàm IF. | `IF(AND(A1>0, B1<10), 1, 0)` | - |
| **Các hàm Xử lý Chuỗi** | `CONCATENATE`, `LEFT`, `RIGHT`, `MID`, `LEN`, `TRIM`, `UPPER`, `LOWER`. | `LEFT(A1, 3)` | - |
| **Các hàm Thời gian** | `DAY`, `MONTH`, `YEAR`, `HOUR`, `MINUTE`, `SECOND`. | `HOUR(A1) * 60` | - |
| **Lỗi cú pháp** | Sẽ được phát hiện ở **Tab QC** và báo lỗi `Invalid Formula`. | - | `IF(A1>B2, 10)` (Thiếu vế) |
| **Lỗi tính toán**| Bắt bằng cây AST, trả về các chuỗi báo lỗi chuẩn Excel (`#DIV/0!`, `#VALUE!`, `#NAME?`, `#ERROR!`).| `A1/0` (Chia cho 0) | - |

---

## 📋 3. Giai đoạn 2: Cấu trúc phân việc chi tiết (Phase 2 - WBS)

### 3.1. Nhóm Models & Core (Dữ liệu & Cấu hình)
- `src/models/config_model.py`: Lớp `AppConfig` (đọc/ghi JSON, quản lý trạng thái mapping).
- `src/models/excel_data_model.py`: Định nghĩa cấu trúc `BrewRecord` (đại diện cho 1 dòng dữ liệu lưu trong RAM).

### 3.2. Nhóm Utils (Tiện ích dùng chung)
- `src/utils/formula_parser.py`: Lớp `ExcelFormulaEvaluator`, phân dịch công thức thành cây Cú pháp AST, hỗ trợ tính toán lười (Lazy Evaluation) và trả mã lỗi Excel.
- `src/utils/theme_manager.py`: Lớp `ThemeManager` tích hợp `darkdetect` (Light/Dark/System).
- `src/utils/qc_logger.py`: Tiện ích hỗ trợ định dạng và ghi danh sách các lỗi QC vào tệp có hậu tố thời gian (vd: `logs/qc_errors_20260518_153000.txt`).

### 3.3. Nhóm Services (Lõi Nghiệp vụ - Không dính dáng đến UI)
- `src/services/excel_reader_service.py`: Hàm `scan_file_qc()` (phát hiện biểu mẫu, check lỗi null/sai vị trí).
- `src/services/excel_sync_service.py`: Lớp `BrewSyncEngine` xử lý luồng Update/Insert trong RAM, sort theo Batch Number, lưu file gốc.

### 3.4. Nhóm Views/Controllers (Giao diện PyQt6)
- `src/views/main_window.py`: Khung cửa sổ chính, thanh trạng thái, menu chọn Theme.
- `src/views/tab_config_system.py`: Lớp khung (Container) ghép nối các widget Cấu hình.
- `src/views/config_widget_profile.py`: Khung quản lý Profile, Tệp đích, và Dấu hiệu nhận diện.
- `src/views/config_widget_mappings.py`: Khung quản lý Lưới Mapping dữ liệu.
- `src/views/tab_qc_check.py`: Tab QC (Kéo thả file, Báo cáo 3 trạng thái: Đạt/Cảnh báo lỗi/Lỗi, Nút xuất log `.txt`).
- `src/views/tab_sync_data.py`: Tab Tổng hợp (Nút bắt đầu chạy, Progress bar).
- `src/views/widget_excel_mockup.py`: Cửa sổ Popup (QDialog) hiển thị lưới Excel ảo để click chọn toạ độ (`C3`, `E4`).
- `src/controllers/worker_threads.py`: Các lớp kế thừa `QThread` (`QCWorker`, `SyncWorker`) để chạy ngầm service, phát tín hiệu (Signals) % tiến độ lên UI.

### 3.5. Nhóm Constants & Exceptions (Hằng số & Ngoại lệ)
- `src/config/constants.py`: Lưu trữ toàn bộ các hằng số (mã màu UI, kích thước, tên sheet mặc định) để tránh Hardcode.
- `src/exceptions/custom_exceptions.py`: Chứa các lỗi tự định nghĩa như `ConfigNotFoundError`, `InvalidTemplateError`, tuân thủ đúng chuẩn.

### 3.6. Nhóm Kiểm thử (Unit Tests)
- `tests/test_formula_parser.py`: Kịch bản test cho bộ dịch công thức (hàm IF, phép tính, lỗi ZeroDivision).
- `tests/test_excel_services.py`: Kịch bản test đối chiếu Số lô SX (Insert/Update) và xử lý file bẩn.

---

## ⚖️ 4. Báo cáo Đối chiếu chéo (Cross-Audit Report)
*Đảm bảo 100% yêu cầu cốt lõi đã được ánh xạ vào mã nguồn thiết kế.*

| Yêu cầu cốt lõi (Theo mô tả) | Hạng mục WBS tương ứng (Tệp / Lớp / Hàm) |
| --- | --- |
| 1. Tự động nhận diện Light/Dark Mode | `src/utils/theme_manager.py` |
| 2. Đọc file không dùng Pandas (giữ nguyên Data Type) | `src/services/excel_reader_service.py` (Chỉ dùng OpenPyXL) |
| 3. Tab Cấu hình: Chọn chế độ quét, quản lý Profile | `src/views/config_widget_profile.py` |
| 4. Tab Cấu hình: Lưới Mapping và Popup click tọa độ | `src/views/config_widget_mappings.py` & `widget_excel_mockup.py` |
| 5. Lõi xử lý: Cây phân dịch (AST) tính toán công thức | `src/utils/formula_parser.py` |
| 6. Tab QC: Kéo thả file, kiểm tra Đa luồng | `src/views/tab_qc_check.py` & `src/controllers/worker_threads.py` |
| 7. Tab QC: Trực quan hóa lỗi thành chữ Đỏ | Logic format UI trong `tab_qc_check.py` |
| 8. Tab Sync: Nhận diện biểu mẫu cũ/mới | Logic nhận diện vân tay trong `excel_reader_service.py` |
| 9. Tab Sync: Đối chiếu Số lô SX (Insert/Update) trên RAM, Sort | `src/services/excel_sync_service.py` (`BrewSyncEngine`) |
| 10. Đóng gói EXE 1 file duy nhất không hiện Console | Lệnh PyInstaller trong `build.py` với cờ `--onefile --windowed` |
| 11. Bổ sung tính năng Lưu log lỗi (.txt) ở Tab QC | `src/utils/qc_logger.py` & `src/views/tab_qc_check.py` |
| 12. Quản lý Lỗi tự tạo (Custom Exceptions) | `src/exceptions/custom_exceptions.py` |
| 13. TDD - Viết test bắt buộc cho Core Logic | Các file trong thư mục `tests/` |

---

## 🚀 5. Lộ trình thi công & To-Do List (Execution Sequence)
Áp dụng mô hình **Outside-In TDD** (Giao diện -> Lõi -> Lưu trữ).

- [x] **Bước 1 (UI/UX - Màn hình chính)**: Dựng khung PyQt6 (`main_window.py`), Theme Manager, và Layout 3 Tab. ➡️ **Kiểm tra**: Chạy thử giao diện và kịch bản `auto_checks.py`.
- [x] **Bước 2 (UI/UX - Cấu hình)**: Dựng Grid cấu hình, Popup chọn tọa độ, Quản lý Profile, và Sách hướng dẫn. ➡️ **Kiểm tra**: Chạy thử click toạ độ, lưu/tải profile, xác nhận file JSON sinh ra chuẩn.
- [x] **Bước 3 (Core - Data Processing)**: Viết TDD (`test_formula_parser.py`) -> Code bộ phân dịch công thức. ➡️ **Kiểm tra**: Chạy `pytest` bắt buộc vượt qua 100%.
- [x] **Bước 4 (Service - QC & Sync)**: Viết TDD (`test_excel_services.py`) -> Code service OpenPyXL đọc/ghi, đối chiếu trên bộ nhớ RAM. ➡️ **Kiểm tra**: Chạy `pytest` ép bẫy lỗi với dữ liệu rác.
- [x] **Bước 5 (Integration)**: Bọc Service vào `QThread`. Nối tín hiệu hiển thị Progress Bar. Tối ưu hóa UI chống giật lag. ➡️ **Kiểm tra**: Chạy `auto_checks.py` toàn dự án và test kéo/thả file thực tế.
- [x] **Bước 6 (Deployment)**: Chạy `build.py` (sẽ tự động clean, test, format) ➡️ **Kiểm tra**: Chạy thử file `.exe` độc lập không cần môi trường Python.

---

## 📝 Nhật ký (Changelog)
- **15/05/2026**: Khởi tạo và chốt thiết kế chi tiết kiến trúc WBS 3 Tab, OpenPyXL, PyQt6 đa luồng.
- **16/05/2026**: Hoàn thành Bước 1 (UI chính) & Bước 2 (Giao diện Cấu hình). Xử lý lỗi sai thư mục `views/` và cập nhật AI_RULES.md.
- **17/05/2026**: Hoàn thành Bước 3 (Formula Parser) & Bước 4 (Dịch vụ Đọc/Ghi Excel).
- **18/05/2026**: Hoàn thành Bước 5 (Tích hợp Đa luồng QThread). Tái cấu trúc Tab Cấu hình, nâng cấp AST Lazy Evaluation và tối ưu báo cáo QC 3 trạng thái.
- **19/05/2026**: Hoàn thành Bước 6. Cập nhật Icon ứng dụng và Đóng gói thành công tệp thực thi độc lập (.exe).
