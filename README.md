# BrewCard_Batch_Updater

Module/Project documentation goes here.

## 🤖 Quy trình Tự động hóa (Workflow & Automation)
Dự án này được sinh ra bởi AI Project Generator và đã được trang bị sẵn các công cụ tự động hóa khắt khe để đảm bảo chất lượng mã nguồn:

| Công cụ / Lệnh | Chức năng tự động thực thi |
| --- | --- |
| **`check.bat`** (hoặc `auto_checks.py`) | 1. **Format Code**: Tự động căn lề chuẩn PEP8 bằng `black`.<br>2. **Auto Architecture**: Quét mã nguồn và vẽ lại cấu trúc vào README.<br>3. **Unit Tests**: Chạy `pytest` kiểm tra logic. |
| **`sync.bat`** | 1. Chạy Auto Checks (Chặn đẩy code nếu có lỗi).<br>2. Tự động tăng version (`version.txt`).<br>3. Commit mã nguồn và đẩy lên GitHub. |
| **`build.bat`** (hoặc `build.py`) | 1. **Clean**: Tự động xóa rác (`__pycache__`, logs, `.env`).<br>2. Chạy Auto Checks bảo vệ mã nguồn.<br>3. Đóng gói thành file `.exe` bằng PyInstaller. |
| **`init_github.bat`** | Tự động khởi tạo Git, tạo Repo trên GitHub bằng CLI, và tạo Release v1.0.0. |
| **`.github/workflows/`** | Tự động chạy Test và Build `.exe` trên mây mỗi khi có code mới đẩy lên. |

> **Lưu ý dành cho AI Assistant (Cursor/Copilot)**:
> Theo quy tắc tại `AI_RULES.md`, AI bắt buộc phải:
> 1. Tự động cập nhật file `PLAN.md` mỗi khi luồng logic hoặc tiến độ thay đổi (Living Documentation).
> 2. Tự động cập nhật `requirements.txt` khi import thư viện mới.

## 💻 Môi trường ảo (.venv)
Nếu bạn đã khởi tạo kèm `.venv`, hãy kích hoạt nó bằng lệnh sau:
- **Windows**: `.\.venv\Scripts\activate`
- **Mac/Linux**: `source .venv/bin/activate`

## 🏗️ Cấu trúc dự án (Architecture)
<!-- ARCHITECTURE_START -->
> Tài liệu này được cập nhật tự động bởi script `scan_architecture.py`.

### 🌳 Cây Thư Mục
```text
📦 BrewCard_Batch_Updater
    ┣ 📜 .dockerignore
    ┣ 📜 .env.example
    ┣ 📜 .gitignore
    ┣ 📜 AI_RULES.md
    ┣ 📜 auto_checks.py
    ┣ 📜 build.bat
    ┣ 📜 build.py
    ┣ 📜 check.bat
    ┣ 📜 docker-compose.yml
    ┣ 📜 Dockerfile
    ┣ 📜 init_github.bat
    ┣ 📜 LICENSE
    ┣ 📜 main.py
    ┣ 📜 PLAN.md
    ┣ 📜 pytest.ini
    ┣ 📜 README.md
    ┣ 📜 requirements.txt
    ┣ 📜 scan_architecture.py
    ┣ 📜 sync.bat
    ┣ 📜 version.txt
    ┣ 📜 migrate_json.py
    ┣ 📜 generate_mocks.py
    ┣ 📜 relink_github.bat
    ┣ 📂 .github
        ┣ 📂 workflows
            ┣ 📜 build.yml
    ┣ 📂 assets
        ┣ 📜 icon0.png
        ┣ 📜 icon1.png
        ┣ 📜 icon3.png
        ┣ 📜 icon4.png
        ┣ 📜 icon.ico
        ┣ 📜 icon.png
    ┣ 📂 data
        ┣ 📜 Dot Graph Syn from BrewCard 2026.xlsx
        ┣ 📜 app_settings.json
        ┣ 📜 BUD Brewcard sync.xlsx
        ┣ 📜 Test.xlsx
        ┣ 📂 profiles
            ┣ 📜 BrewCard_FormNew.json
            ┣ 📜 BrewCard_FormOld.json
    ┣ 📂 src
        ┣ 📜 __init__.py
        ┣ 📂 config
            ┣ 📜 __init__.py
            ┣ 📜 constants.py
        ┣ 📂 controllers
            ┣ 📜 __init__.py
            ┣ 📜 worker_threads.py
        ┣ 📂 exceptions
            ┣ 📜 __init__.py
            ┣ 📜 custom_exceptions.py
        ┣ 📂 models
            ┣ 📜 __init__.py
            ┣ 📜 config_model.py
            ┣ 📜 excel_data_model.py
            ┣ 📜 alias_memory.py
        ┣ 📂 services
            ┣ 📜 __init__.py
            ┣ 📜 excel_reader_service.py
            ┣ 📜 excel_sync_service.py
        ┣ 📂 utils
            ┣ 📜 __init__.py
            ┣ 📜 core_utils.py
            ┣ 📜 formula_parser.py
            ┣ 📜 qc_logger.py
            ┣ 📜 retry_example.py
            ┣ 📜 theme_manager.py
        ┣ 📂 views
            ┣ 📜 config_widget_mappings.py
            ┣ 📜 config_widget_profile.py
            ┣ 📜 dialog_guide.py
            ┣ 📜 main_window.py
            ┣ 📜 tab_config_system.py
            ┣ 📜 tab_qc_check.py
            ┣ 📜 tab_sync_data.py
            ┣ 📜 widget_excel_mockup.py
            ┣ 📜 widget_noscroll_combobox.py
            ┣ 📜 config_dialog_alias.py
            ┣ 📜 dialog_column_selector.py
            ┣ 📜 __init__.py
    ┣ 📂 tests
        ┣ 📜 test_BrewCard_Batch_Updater.py
        ┣ 📜 test_excel_services.py
        ┣ 📜 test_formula_parser.py
        ┣ 📜 test_config_model.py
        ┣ 📜 test_alias_memory.py
        ┣ 📜 test_e2e_workflow.py
        ┣ 📂 test_data
            ┣ 📜 mock_input_batch.xlsx
            ┣ 📜 mock_input_clean.xlsx
            ┣ 📜 mock_input_dirty.xlsx
            ┣ 📜 mock_input_clean_update.xlsx
            ┣ 📜 mock_input_complex_formulas.xlsx
            ┣ 📜 mock_input_dirty_wrong_form.xlsx
            ┣ 📜 mock_master.xlsx
    ┣ 📂 .pytest_cache
        ┣ 📜 README.md
        ┣ 📜 .gitignore
        ┣ 📜 CACHEDIR.TAG
        ┣ 📂 v
            ┣ 📂 cache
                ┣ 📜 nodeids
                ┣ 📜 lastfailed
    ┣ 📂 output
        ┣ 📜 E2E_Dirty_Path_Result.xlsx
        ┣ 📜 E2E_Happy_Path_Result.xlsx
```
### 🧩 Chi Tiết Modules (Tổng quan)

| 📄 Tệp tin (File) | 📝 Chức năng / Mô tả |
| --- | --- |
| `auto_checks.py` | Công cụ tự động kiểm tra, format code, cập nhật tài liệu và chạy test trước khi commit/build. |
| `build.py` | Kịch bản tự động hóa quá trình đóng gói ứng dụng bằng PyInstaller. |
| `generate_mocks.py` | Script hỗ trợ tạo các file Excel giả lập phục vụ kiểm thử E2E. |
| `main.py` | Điểm bắt đầu (Entry point) của dự án BrewCard_Batch_Updater. |
| `migrate_json.py` | Chưa có mô tả chi tiết. |
| `scan_architecture.py` | Script tự động quét thư mục dự án và sinh báo cáo kiến trúc. |
| `src/config/constants.py` | Cấu hình trung tâm lưu trữ các hằng số của ứng dụng. |
| `src/controllers/worker_threads.py` | Các luồng chạy ngầm để xử lý tác vụ nền. |
| `src/exceptions/custom_exceptions.py` | Các lớp ngoại lệ tự định nghĩa cho ứng dụng. |
| `src/models/alias_memory.py` | Hệ thống bộ nhớ cho việc ghép nối tên cột, học hỏi từ lựa chọn của người dùng. |
| `src/models/config_model.py` | Mô hình dữ liệu cấu hình ứng dụng. |
| `src/models/excel_data_model.py` | Mô hình dữ liệu Excel trong bộ nhớ RAM. |
| `src/services/excel_reader_service.py` | Dịch vụ đọc file Excel phục vụ kiểm tra chất lượng (QC). |
| `src/services/excel_sync_service.py` | Dịch vụ đồng bộ Excel để cập nhật file Tổng. |
| `src/utils/core_utils.py` | Các hàm tiện ích lõi bao gồm xử lý đường dẫn và thử lại I/O. |
| `src/utils/formula_parser.py` | Bộ phân dịch và tính toán công thức Excel. |
| `src/utils/qc_logger.py` | Tiện ích ghi log lỗi QC. |
| `src/utils/retry_example.py` | Chưa có mô tả chi tiết. |
| `src/utils/theme_manager.py` | Quản lý giao diện (Theme) cho ứng dụng PyQt6. |
| `src/views/config_dialog_alias.py` | Hộp thoại cảnh báo ghép nối thủ công cho các cột không rõ tên. |
| `src/views/config_widget_mappings.py` | Widget quản lý bảng lưới ánh xạ dữ liệu. |
| `src/views/config_widget_profile.py` | Widget quản lý cấu hình Profile và File Đích. |
| `src/views/dialog_column_selector.py` | Hộp thoại chọn cột thủ công nếu tự động nhận diện thất bại. |
| `src/views/dialog_guide.py` | Hộp thoại hiển thị hướng dẫn sử dụng chi tiết và cú pháp công thức. |
| `src/views/main_window.py` | Cửa sổ chính của ứng dụng. |
| `src/views/tab_config_system.py` | Phân hệ Cấu hình Hệ thống. |
| `src/views/tab_qc_check.py` | Phân hệ Kiểm tra Chất lượng (QC). |
| `src/views/tab_sync_data.py` | Phân hệ Tổng hợp và Gộp Dữ liệu. |
| `src/views/widget_excel_mockup.py` | Giao diện mô phỏng Excel để chọn tọa độ ô. |
| `src/views/widget_noscroll_combobox.py` | Lớp QComboBox tùy chỉnh bỏ qua sự kiện cuộn chuột. |
| `tests/test_alias_memory.py` | Kiểm thử mô hình bộ nhớ ghép nối cột. |
| `tests/test_BrewCard_Batch_Updater.py` | Chưa có mô tả chi tiết. |
| `tests/test_config_model.py` | Kiểm thử đơn vị cho mô hình dữ liệu cấu hình ứng dụng. |
| `tests/test_e2e_workflow.py` | Kiểm thử tích hợp toàn trình (E2E) trong môi trường Hộp cát (Sandbox). |
| `tests/test_excel_services.py` | Kiểm thử đơn vị cho các dịch vụ xử lý Excel. |
| `tests/test_formula_parser.py` | Các bài kiểm thử đơn vị cho bộ phân dịch công thức Excel. |

### 📚 Tài liệu API & Logic chi tiết (Dành cho Dev/AI)
Phần này trích xuất tự động thông tin về Đầu vào (Inputs) và Đầu ra (Outputs) của các hàm/lớp trong từng module để hỗ trợ tích hợp và phát triển.

#### 📄 `auto_checks.py`
**Functions:**

- **`def run_cmd(cmd: str, desc: str) -> None`**
  > Thực thi một lệnh shell hệ thống và kiểm tra lỗi.
  > - Inputs:
  >   + cmd (str): Lệnh shell cần thực thi.
  >   + desc (str): Mô tả hiển thị trên màn hình.
  > - Outputs: Không trả về giá trị (None). Sẽ dừng chương trình bằng sys.exit(1) nếu lệnh thất bại.

- **`def main() -> None`**
  > Hàm chính điều phối chuỗi kiểm tra tự động bao gồm: Định dạng mã nguồn (Black), Cập nhật Kiến trúc (Scan), và Chạy Test (Pytest).


#### 📄 `build.py`
**Functions:**

- **`def get_next_version(file_path: str, bump_type: str) -> str`**
  > Chưa có mô tả.

- **`def create_version_file(version: str) -> str`**
  > Chưa có mô tả.

- **`def clean_pycache(start_path: str) -> None`**
  > Chưa có mô tả.

- **`def clean_logs(start_path: str) -> None`**
  > Chưa có mô tả.

- **`def clean_temp_files(start_path: str) -> None`**
  > Chưa có mô tả.

- **`def ensure_init_files() -> None`**
  > Chưa có mô tả.

- **`def build_app() -> None`**
  > Chưa có mô tả.


#### 📄 `generate_mocks.py`
**Functions:**

- **`def generate_mocks() -> Any`**
  > Chưa có mô tả.


#### 📄 `main.py`
**Functions:**

- **`def main() -> Any`**
  > Chưa có mô tả.


#### 📄 `migrate_json.py`
**Functions:**

- **`def guess_format(name: str) -> str`**
  > Chưa có mô tả.

- **`def run_migration() -> Any`**
  > Chưa có mô tả.


#### 📄 `scan_architecture.py`
**Functions:**

- **`def get_directory_tree(start_path: str, exclude_dirs: set) -> str`**
  > Sinh cây thư mục (bỏ qua các thư mục không cần thiết).

- **`def parse_python_file(file_path: str) -> dict`**
  > Phân tích file Python bằng AST để lấy thông tin Class, Function và Docstring.

- **`def update_readme(target_dir: str, readme_file: str) -> None`**
  > Quét kiến trúc và cập nhật thẳng vào file README.md.


#### 📄 `src/controllers/worker_threads.py`
**Classes:**

- **`class QCWorker`**
  > EN: Worker thread for running QC scans on multiple files.
  > VI: Luồng chạy ngầm để quét QC trên nhiều tệp.
  - **`def __init__(file_sheets_map: Dict[str, List[str]], config: AppConfig, parent) -> Any`**
    > Chưa có mô tả.
  - **`def run() -> None`**
    > EN: Start the QC scanning process. VI: Bắt đầu quá trình quét QC.

- **`class SyncWorker`**
  > EN: Worker thread for syncing data to the master file.
  > VI: Luồng chạy ngầm để đồng bộ dữ liệu vào tệp master.
  - **`def __init__(records: List[BrewRecord], config: AppConfig, parent) -> Any`**
    > Chưa có mô tả.
  - **`def run() -> None`**
    > EN: Start the sync process. VI: Bắt đầu quá trình đồng bộ.


#### 📄 `src/exceptions/custom_exceptions.py`
**Classes:**

- **`class ConfigNotFoundError`**
  > EN: Raised when a configuration profile is not found. VI: Lỗi khi không tìm thấy hồ sơ cấu hình.

- **`class InvalidTemplateError`**
  > EN: Raised when an input Excel file does not match the expected template. VI: Lỗi khi tệp Excel đầu vào không khớp với mẫu.


#### 📄 `src/models/alias_memory.py`
**Classes:**

- **`class AliasMemory`**
  > EN: Manages loading and saving user-mapped aliases. VI: Quản lý tên cột học được.
  - **`def __init__() -> Any`**
    > Chưa có mô tả.
  - **`def load() -> None`**
    > EN: Load memory from JSON. VI: Tải bộ nhớ từ JSON.
  - **`def save() -> None`**
    > EN: Save memory to JSON. VI: Lưu bộ nhớ xuống JSON.
  - **`def add_alias(unknown_name: str, target_name: str) -> None`**
    > Chưa có mô tả.
  - **`def get_target(unknown_name: str) -> Optional[str]`**
    > Chưa có mô tả.


#### 📄 `src/models/config_model.py`
**Classes:**

- **`class AppConfig`**
  > EN: Manages loading and saving configuration to a JSON file.
  > VI: Quản lý tải và lưu cấu hình vào tệp JSON.
  - **`def __init__(profile_name: str) -> Any`**
    > Chưa có mô tả.
  - **`def _migrate_old_config() -> None`**
    > EN: Migrate old config to multi-profile. VI: Chuyển đổi cấu hình cũ sang hệ thống mới.
  - **`def _get_default_data() -> Dict[str, Any]`**
    > Chưa có mô tả.
  - **`def _get_last_profile() -> str`**
    > Chưa có mô tả.
  - **`def _save_last_profile() -> None`**
    > Chưa có mô tả.
  - **`def load() -> None`**
    > EN: Load JSON from file. VI: Tải dữ liệu từ tệp JSON.
  - **`def save() -> None`**
    > EN: Save data to JSON. VI: Lưu dữ liệu xuống tệp JSON.
  - **`def delete_profile() -> bool`**
    > EN: Delete current profile. VI: Xóa cấu hình hiện tại.
  - **`def get_all_profiles() -> List[str]`**
    > EN: Get all saved profiles. VI: Lấy danh sách tất cả các cấu hình.


#### 📄 `src/models/excel_data_model.py`
**Classes:**

- **`class BrewRecord`**
  > EN: Represents a single parsed row of BrewCard data.
  > VI: Đại diện cho một dòng dữ liệu BrewCard đã được phân tích.


#### 📄 `src/services/excel_reader_service.py`
**Functions:**

- **`def _safe_load_workbook(file_path: str, data_only: bool) -> Any`**
  > EN: Load workbook with retry mechanism. VI: Mở tệp Excel kèm cơ chế thử lại.

- **`def _check_fingerprint(ws, rule_str: str) -> bool`**
  > EN: Check if the worksheet matches the fingerprint rule. VI: Kiểm tra xem sheet có khớp dấu vân tay không.

- **`def get_sheet_names(file_path: str) -> List[str]`**
  > EN: Get all sheet names from an Excel file safely. VI: Lấy danh sách tên sheet.

- **`def get_sheet_preview(file_path: str, sheet_name: str, max_rows: int) -> List[List[Any]]`**
  > EN: Get preview data from sheet. VI: Lấy tối đa 20 dòng để xem trước.

- **`def extract_formulas_from_sheet(file_path: str, sheet_name: str, manual_name_col: int, manual_form_col: int, manual_start_row: int) -> List[Tuple[str, str]]`**
  > EN: Extract raw (name, formula) pairs from a specific sheet. VI: Trích xuất tên và công thức.

- **`def normalize_name(text: str) -> str`**
  > EN: Normalize string by removing extra spaces and lowercasing. VI: Chuẩn hóa chuỗi.

- **`def sanitize_formula(formula: Any) -> str`**
  > EN: Clean external links from formula. VI: Xóa liên kết ngoại lai khỏi công thức.

- **`def process_import_mappings(extracted_data: List[Tuple[str, str]], target_names: List[str]) -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]], int]`**
  > EN: Process extracted data into exact matches and pending aliases. VI: Phân loại dữ liệu trích xuất.

- **`def scan_file_qc(file_path: str, config: AppConfig, target_sheets: List[str]) -> Tuple[bool, List[str], List[Dict[str, Any]]]`**
  > EN: Scan input file, validate against config, and extract mapped values.
  > VI: Quét file đầu vào, kiểm tra hợp lệ theo cấu hình, và trích xuất dữ liệu.
  > Returns: (is_valid, list_of_errors, list_of_extracted_data_dicts)


#### 📄 `src/services/excel_sync_service.py`
**Classes:**

- **`class BrewSyncEngine`**
  > EN: Engine handling Insert/Update logic. VI: Động cơ xử lý chèn/cập nhật.
  - **`def __init__(config: AppConfig) -> Any`**
    > Chưa có mô tả.
  - **`def _find_batch_column() -> str`**
    > EN: Find the column letter for the batch number. VI: Tìm chữ cái của cột Số lô.
  - **`def sync_records(records: List[BrewRecord]) -> bool`**
    > EN: Sync records into the target master file (Insert/Update/Sort).
    > VI: Đồng bộ danh sách dữ liệu vào file tổng (Thêm mới/Cập nhật/Sắp xếp).


#### 📄 `src/utils/core_utils.py`
**Functions:**

- **`def get_project_root() -> str`**
  > EN: Get safe project root path (handles PyInstaller).
  > VI: Lấy đường dẫn gốc dự án an toàn (xử lý khi đóng gói bằng PyInstaller).

- **`def retry_io(retries: int, delay: float) -> Any`**
  > EN: Retry decorator for I/O operations to handle transient errors/locks.
  > VI: Decorator thử lại cho các tác vụ I/O để xử lý lỗi tạm thời/tệp bị khóa.


#### 📄 `src/utils/formula_parser.py`
**Classes:**

- **`class ExcelFormulaEvaluator`**
  > EN: A class to parse and evaluate Excel-like formulas.
  > VI: Lớp phân dịch (AST) dùng để tính toán các công thức kiểu Excel.
  - **`def __init__(worksheet: Worksheet) -> Any`**
    > Chưa có mô tả.
  - **`def evaluate(formula: str) -> Any`**
    > EN: Evaluate the given formula string. VI: Tính toán giá trị của chuỗi công thức được cho.
  - **`def _match() -> Any`**
    > Chưa có mô tả.
  - **`def _to_num(val: Any) -> float`**
    > EN: Safe cast to float (handles Excel Date). VI: Ép kiểu an toàn sang số.
  - **`def _flatten_args(args: List[Any]) -> List[Any]`**
    > Chưa có mô tả.
  - **`def _eval_node(node: Any) -> Any`**
    > EN: Evaluate the AST node. VI: Tính toán giá trị từ cây AST.
  - **`def _parse_expr() -> Any`**
    > Chưa có mô tả.
  - **`def _parse_comp() -> Any`**
    > Chưa có mô tả.
  - **`def _parse_concat() -> Any`**
    > Chưa có mô tả.
  - **`def _parse_add() -> Any`**
    > Chưa có mô tả.
  - **`def _parse_mul() -> Any`**
    > Chưa có mô tả.
  - **`def _parse_exp() -> Any`**
    > Chưa có mô tả.
  - **`def _parse_unary() -> Any`**
    > Chưa có mô tả.
  - **`def _parse_percentage() -> Any`**
    > Chưa có mô tả.
  - **`def _parse_primary() -> Any`**
    > Chưa có mô tả.
  - **`def _evaluate_function(func_name: str, args: List[Any]) -> Any`**
    > Chưa có mô tả.
  - **`def _get_cell_value(coord: str) -> Any`**
    > Chưa có mô tả.
  - **`def _get_range_values(range_str: str) -> List[Any]`**
    > Chưa có mô tả.


#### 📄 `src/utils/qc_logger.py`
**Functions:**

- **`def log_qc_errors(errors_map: Dict[str, List[str]]) -> str`**
  > EN: Logs QC errors to a timestamped file and returns the file path.
  > VI: Ghi lại các lỗi QC vào một tệp có dấu thời gian và trả về đường dẫn tệp.


#### 📄 `src/utils/theme_manager.py`
**Classes:**

- **`class ThemeManager`**
  > EN: Handles switching between Light, Dark, and System themes.
  > VI: Xử lý chuyển đổi giữa các giao diện Sáng, Tối và Hệ thống.
  - **`def apply_theme(app: QApplication, mode: str) -> None`**
    > EN: Apply the selected theme to the application.
    > VI: Áp dụng giao diện được chọn cho ứng dụng.
  - **`def _apply_dark_theme(app: QApplication) -> None`**
    > EN: Apply dark palette. VI: Áp dụng bảng màu tối.
  - **`def _apply_light_theme(app: QApplication) -> None`**
    > EN: Reset to default light palette. VI: Khôi phục bảng màu sáng mặc định.


#### 📄 `src/views/config_dialog_alias.py`
**Classes:**

- **`class AliasMappingDialog`**
  > EN: Dialog for manually mapping unmatched columns during import.
  > VI: Hộp thoại cho phép người dùng chọn Cột đích thủ công cho các tên cột không khớp.
  - **`def __init__(pending_aliases: list, target_info: dict, parent) -> Any`**
    > Chưa có mô tả.
  - **`def _setup_ui() -> Any`**
    > Chưa có mô tả.
  - **`def get_results() -> dict`**
    > EN: Return a dict of mapped aliases. VI: Trả về từ điển kết quả ghép nối.


#### 📄 `src/views/config_widget_mappings.py`
**Classes:**

- **`class ConfigWidgetMappings`**
  > Chưa có mô tả.
  - **`def __init__(parent) -> Any`**
    > Chưa có mô tả.
  - **`def _setup_ui() -> Any`**
    > Chưa có mô tả.
  - **`def _on_cell_changed(row: int, col: int) -> Any`**
    > Chưa có mô tả.
  - **`def update_headers(letter_to_name: dict) -> Any`**
    > Chưa có mô tả.
  - **`def _update_target_name(row: int, col_letter: str) -> Any`**
    > Chưa có mô tả.
  - **`def _update_target_name_by_cmb(cmb: QComboBox, col_letter: str) -> Any`**
    > Chưa có mô tả.
  - **`def _add_mapping_row(target_col: str, target_letter: str, source_mapping: str, format_type: str, scroll_to_bottom: bool) -> Any`**
    > Chưa có mô tả.
  - **`def _delete_mapping_row(btn: QPushButton) -> Any`**
    > Chưa có mô tả.
  - **`def _open_excel_mockup() -> Any`**
    > Chưa có mô tả.
  - **`def _import_formulas_from_file() -> Any`**
    > Chưa có mô tả.
  - **`def load_mappings(mappings: list) -> Any`**
    > Chưa có mô tả.
  - **`def get_mappings() -> list`**
    > Chưa có mô tả.


#### 📄 `src/views/config_widget_profile.py`
**Classes:**

- **`class ConfigWidgetProfile`**
  > Chưa có mô tả.
  - **`def __init__(parent) -> Any`**
    > Chưa có mô tả.
  - **`def _setup_ui() -> Any`**
    > Chưa có mô tả.
  - **`def _setup_connections() -> Any`**
    > Chưa có mô tả.
  - **`def _on_target_path_edited() -> Any`**
    > Chưa có mô tả.
  - **`def _update_chain_preview() -> Any`**
    > Chưa có mô tả.
  - **`def _safe_load_workbook(file_path: str, read_only: bool, data_only: bool) -> Any`**
    > Chưa có mô tả.
  - **`def _browse_target_file() -> Any`**
    > Chưa có mô tả.
  - **`def _populate_sheet_names(file_path: str, default_sheet: str) -> Any`**
    > Chưa có mô tả.
  - **`def _refresh_headers() -> Any`**
    > Chưa có mô tả.
  - **`def load_data(config_data: dict, current_profile: str, all_profiles: list) -> Any`**
    > Chưa có mô tả.
  - **`def get_data() -> dict`**
    > Chưa có mô tả.


#### 📄 `src/views/dialog_column_selector.py`
**Classes:**

- **`class ColumnSelectorDialog`**
  > EN: Lets user select Name/Formula columns from a data preview.
  > VI: Cho phép người dùng chọn cột Tên/Công thức từ bảng xem trước.
  - **`def __init__(preview_data: List[List[str]], parent) -> Any`**
    > Chưa có mô tả.
  - **`def _setup_ui() -> Any`**
    > Chưa có mô tả.
  - **`def get_selection() -> Tuple[int, int, int]`**
    > EN: Returns (name_col_idx, form_col_idx, start_row). VI: Trả về (chỉ số cột Tên, chỉ số cột Form, dòng bắt đầu).


#### 📄 `src/views/dialog_guide.py`
**Classes:**

- **`class GuideDialog`**
  > EN: Dialog showing comprehensive user guide and formula syntax.
  > VI: Hộp thoại hiển thị hướng dẫn sử dụng chi tiết và cú pháp công thức.
  - **`def __init__(parent: QWidget | None) -> None`**
    > Chưa có mô tả.


#### 📄 `src/views/main_window.py`
**Classes:**

- **`class MainWindow`**
  > EN: The main application window containing the tab widget and menus.
  > VI: Cửa sổ ứng dụng chính chứa các thẻ (tabs) và thanh thực đơn.
  - **`def __init__() -> Any`**
    > Chưa có mô tả.
  - **`def _setup_ui() -> None`**
    > EN: Setup central widget and tabs. VI: Thiết lập giao diện trung tâm và các thẻ.
  - **`def _setup_menu() -> None`**
    > EN: Setup the menu bar for themes. VI: Thiết lập thanh thực đơn chuyển đổi giao diện.
  - **`def _change_theme(mode: str) -> None`**
    > Chưa có mô tả.


#### 📄 `src/views/tab_config_system.py`
**Classes:**

- **`class TabConfigSystem`**
  > EN: Widget for the System Configuration Tab.
  > VI: Lớp giao diện cho Thẻ Cấu hình Hệ thống.
  - **`def __init__(parent: QWidget | None) -> None`**
    > Chưa có mô tả.
  - **`def _setup_ui() -> None`**
    > EN: Initialize the UI layout. VI: Khởi tạo bố cục giao diện.
  - **`def _setup_connections() -> None`**
    > EN: Setup signal connections. VI: Cài đặt các tín hiệu nối 2 Widget.
  - **`def _load_profile(profile_name: str) -> None`**
    > EN: Load selected profile. VI: Tải cấu hình được chọn.
  - **`def _delete_profile(profile_name: str) -> None`**
    > EN: Delete profile. VI: Xóa cấu hình.
  - **`def _load_data_to_ui() -> None`**
    > EN: Load data to UI. VI: Tải dữ liệu lên giao diện.
  - **`def _save_config() -> None`**
    > EN: Save UI data to JSON. VI: Lưu dữ liệu từ UI xuống JSON.


#### 📄 `src/views/tab_qc_check.py`
**Classes:**

- **`class SheetSelectionDialog`**
  > Chưa có mô tả.
  - **`def __init__(file_name: str, all_sheets: List[str], selected_sheets: List[str], parent) -> Any`**
    > Chưa có mô tả.
  - **`def _set_check_all(state: Qt.CheckState) -> Any`**
    > Chưa có mô tả.
  - **`def get_selected_sheets() -> List[str]`**
    > Chưa có mô tả.

- **`class TabQCCheck`**
  > EN: Widget for the Quality Control Check Tab.
  > VI: Lớp giao diện cho Thẻ Kiểm tra Chất lượng.
  - **`def __init__(parent: QWidget | None) -> None`**
    > Chưa có mô tả.
  - **`def _setup_ui() -> None`**
    > EN: Initialize the UI layout. VI: Khởi tạo bố cục giao diện.
  - **`def _setup_connections() -> None`**
    > EN: Setup signal-slot connections. VI: Kết nối các tín hiệu.
  - **`def dragEnterEvent(event) -> None`**
    > Chưa có mô tả.
  - **`def dragLeaveEvent(event) -> None`**
    > Chưa có mô tả.
  - **`def dropEvent(event) -> None`**
    > Chưa có mô tả.
  - **`def _update_progress(percentage: int, file_name: str) -> None`**
    > Chưa có mô tả.
  - **`def _update_file_status(file_path: str, is_valid: bool, errors: List[str], data_list: List[Dict[str, Any]]) -> None`**
    > Chưa có mô tả.
  - **`def _on_qc_finished() -> None`**
    > Chưa có mô tả.
  - **`def _start_scan() -> None`**
    > Chưa có mô tả.
  - **`def _clear_list() -> None`**
    > Chưa có mô tả.
  - **`def _export_errors() -> None`**
    > Chưa có mô tả.
  - **`def _add_files_to_table(file_paths: List[str]) -> None`**
    > Chưa có mô tả.
  - **`def _open_sheet_selector(file_path: str, row: int) -> Any`**
    > Chưa có mô tả.
  - **`def _find_row_by_path(file_path: str) -> int | None`**
    > Chưa có mô tả.


#### 📄 `src/views/tab_sync_data.py`
**Classes:**

- **`class TabSyncData`**
  > EN: Widget for the Data Synchronization Tab.
  > VI: Lớp giao diện cho Thẻ Tổng hợp Dữ liệu.
  - **`def __init__(parent: QWidget | None) -> None`**
    > Chưa có mô tả.
  - **`def _setup_ui() -> None`**
    > EN: Initialize the UI layout. VI: Khởi tạo bố cục giao diện.
  - **`def on_qc_scan_completed(records: List[BrewRecord]) -> None`**
    > EN: Slot to receive valid records from the QC tab.
    > VI: Slot nhận dữ liệu hợp lệ từ tab QC.
  - **`def _start_sync() -> None`**
    > EN: Start the sync process. VI: Bắt đầu quá trình đồng bộ.
  - **`def _on_sync_finished(success: bool, message: str) -> None`**
    > EN: Handle sync finished. VI: Xử lý khi đồng bộ hoàn tất.


#### 📄 `src/views/widget_excel_mockup.py`
**Classes:**

- **`class WidgetExcelMockup`**
  > EN: Dialog showing a grid to pick an Excel cell coordinate (e.g., C3).
  > VI: Hộp thoại hiển thị lưới để chọn tọa độ ô Excel (vd: C3).
  - **`def __init__(parent) -> Any`**
    > Chưa có mô tả.
  - **`def _setup_ui() -> None`**
    > EN: Initialize the UI layout. VI: Khởi tạo bố cục giao diện.
  - **`def _on_accept() -> None`**
    > EN: Handle accept button. VI: Xử lý sự kiện nút xác nhận hoặc click đúp.


#### 📄 `src/views/widget_noscroll_combobox.py`
**Classes:**

- **`class NoScrollComboBox`**
  > EN: Custom QComboBox that ignores mouse wheel scrolling.
  > VI: Lớp QComboBox tùy chỉnh bỏ qua sự kiện cuộn chuột để tránh thay đổi dữ liệu ngoài ý muốn.
  - **`def __init__(parent: QWidget | None) -> None`**
    > Chưa có mô tả.
  - **`def wheelEvent(event: QWheelEvent) -> None`**
    > Chưa có mô tả.


#### 📄 `tests/test_alias_memory.py`
**Functions:**

- **`def test_alias_memory_operations(tmp_path, monkeypatch) -> Any`**
  > EN: Test saving and loading alias memory. VI: Kiểm thử lưu/tải bộ nhớ.


#### 📄 `tests/test_BrewCard_Batch_Updater.py`
**Functions:**

- **`def test_example() -> Any`**
  > EN: Example test to enforce TDD.
  > VI: Test mẫu để ép tuân thủ TDD.


#### 📄 `tests/test_config_model.py`
**Functions:**

- **`def temp_env(tmp_path, monkeypatch) -> Any`**
  > EN: Mock the working directory to prevent overriding real config files.
  > VI: Giả lập thư mục làm việc để không ghi đè lên tệp cấu hình thật.

- **`def test_app_config_create_and_save(temp_env) -> Any`**
  > EN: Test creating and saving a new profile. VI: Kiểm thử tạo và lưu hồ sơ mới.

- **`def test_app_config_load(temp_env) -> Any`**
  > EN: Test loading an existing profile. VI: Kiểm thử tải hồ sơ đã tồn tại.

- **`def test_app_config_delete(temp_env) -> Any`**
  > EN: Test deleting a profile. VI: Kiểm thử xóa hồ sơ.

- **`def test_app_config_get_all_profiles(temp_env) -> Any`**
  > EN: Test retrieving all profiles. VI: Kiểm thử lấy danh sách toàn bộ hồ sơ.


#### 📄 `tests/test_e2e_workflow.py`
**Functions:**

- **`def sandbox_env(tmp_path) -> Any`**
  > EN: Setup sandbox environment with user's real mock files.
  > VI: Thiết lập môi trường hộp cát với các file mẫu thật của người dùng.

- **`def test_e2e_happy_path(sandbox_env) -> Any`**
  > EN: Test Happy Path (Clean Data).
  > VI: Kiểm thử luồng dữ liệu sạch (Happy Path), không có lỗi.

- **`def test_e2e_dirty_path(sandbox_env) -> Any`**
  > EN: Test Dirty Path (Error Data).
  > VI: Kiểm thử luồng dữ liệu lỗi (Dirty Path). Hệ thống PHẢI TỪ CHỐI ghi.

- **`def test_e2e_import_formulas_from_excel(tmp_path) -> Any`**
  > EN: E2E test for extracting and processing formulas from a real Excel file.
  > VI: Kiểm thử E2E cho việc trích xuất và xử lý công thức từ file Excel thật.

- **`def test_e2e_update_overwrite(sandbox_env) -> Any`**
  > EN: Test updating/overwriting an existing batch record.
  > VI: Kiểm thử luồng Ghi đè cập nhật mẻ nấu đã tồn tại.

- **`def test_e2e_complex_formulas(sandbox_env) -> Any`**
  > EN: Test parsing and calculating complex AST formulas.
  > VI: Kiểm thử việc phân dịch các công thức phức tạp qua AST.

- **`def test_e2e_wrong_fingerprint(sandbox_env) -> Any`**
  > EN: Test rejection of files that do not match the fingerprint.
  > VI: Kiểm thử việc từ chối các file không khớp dấu vân tay nhận diện.


#### 📄 `tests/test_excel_services.py`
**Functions:**

- **`def mock_config(tmp_path) -> Any`**
  > Chưa có mô tả.

- **`def test_scan_file_not_found(mock_config) -> Any`**
  > Chưa có mô tả.

- **`def test_scan_file_wrong_sheet(tmp_path, mock_config) -> Any`**
  > Chưa có mô tả.

- **`def test_scan_file_success(tmp_path, mock_config) -> Any`**
  > Chưa có mô tả.

- **`def test_sync_engine_insert_update_sort(tmp_path, mock_config) -> Any`**
  > Chưa có mô tả.

- **`def test_normalize_name() -> Any`**
  > EN: Test string normalization. VI: Kiểm thử tính năng chuẩn hóa chuỗi.

- **`def test_process_import_mappings() -> Any`**
  > EN: Test separating extracted data into exact matches and pending aliases.
  > VI: Kiểm thử chức năng phân tách dữ liệu thành danh sách khớp chuẩn và danh sách chờ ghép nối.

- **`def test_sanitize_formula() -> Any`**
  > EN: Test cleaning formulas. VI: Kiểm thử làm sạch công thức.


#### 📄 `tests/test_formula_parser.py`
**Classes:**

- **`class MockCell`**
  > EN: Mock cell object. VI: Đối tượng cell giả.
  - **`def __init__(value) -> Any`**
    > Chưa có mô tả.

**Functions:**

- **`def create_mock_sheet(data: dict) -> MagicMock`**
  > EN: Creates a mock worksheet that can be accessed like openpyxl.
  > VI: Tạo một worksheet giả có thể truy cập như openpyxl.

- **`def evaluator() -> ExcelFormulaEvaluator`**
  > EN: Provides an evaluator instance. VI: Cung cấp một đối tượng evaluator.

- **`def test_formula_evaluation(evaluator: ExcelFormulaEvaluator, formula: str, expected: any) -> Any`**
  > EN: Tests various valid formulas. VI: Kiểm thử các công thức hợp lệ.

- **`def test_formula_errors(evaluator: ExcelFormulaEvaluator, formula: str, expected_error_str: str) -> Any`**
  > EN: Tests formulas that should return error strings. VI: Kiểm thử các công thức trả về chuỗi lỗi.

<!-- ARCHITECTURE_END -->
