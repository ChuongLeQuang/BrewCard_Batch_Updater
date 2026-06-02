# AI_RULES.md (Python Full Version)

## 0. AI System Instructions / Nguyên tắc cốt lõi cho AI
- **Bắt buộc đọc tài liệu (Pre-computation reading)**:
  1. Luôn ưu tiên đọc và tuân thủ chặt chẽ file `AI_RULES.md` này trước khi phân tích logic hay viết bất kỳ dòng mã nào.
  2. Chủ động tìm và đọc các file hoạch định dự án cốt lõi (như `PLAN.md`, `PROJECT_PLAN.md`, hoặc `README.md` ở thư mục gốc) để hiểu rõ bối cảnh, luồng nghiệp vụ và tiến độ dự án.
  3. Đối với các file `.md` tài liệu khác, **chỉ đọc khi chúng thực sự liên quan** đến task đang xử lý (VD: tài liệu API, doc của module cụ thể) hoặc khi được người dùng yêu cầu rõ ràng, tránh việc đọc tràn lan làm phân tán ngữ cảnh.
- **Cập nhật tài liệu liên tục (Living Documentation)**: Kế hoạch (`PLAN.md`) không phải là tệp tĩnh. Bất cứ khi nào trong quá trình code phát sinh vấn đề mới, thay đổi luồng logic, hoặc thêm/bớt tính năng so với dự kiến ban đầu, AI **bắt buộc phải chủ động cập nhật lại file `PLAN.md`** để đảm bảo tài liệu luôn phản ánh đúng 100% thực tế của codebase.
- **Quy tắc lập kế hoạch (Planning & WBS Rules)**:
  1. **Chi tiết hóa tối đa (Granularity)**: Tuyệt đối không sử dụng các gạch đầu dòng chung chung trong `PLAN.md` (VD: "Khởi tạo dự án", "Xây dựng Models", "Làm UI"). Bắt buộc phải phân rã công việc thành WBS (Work Breakdown Structure) chi tiết đến mức liệt kê rõ từng tệp tin (file), lớp (class), hàm (function), API endpoint, và thậm chí là **từng trường dữ liệu (field/attribute), kiểu dữ liệu (dtype nếu cần)** cụ thể cần tạo.
  2. **Hoàn thiện Thiết kế (Design First)**: Tuyệt đối không bước sang Giai đoạn Viết mã (Phase 2 - Development) nếu Giai đoạn Thiết kế (Phase 1) chưa hoàn thiện 100%. Phase 1 phải bao phủ đầy đủ: Luồng dữ liệu (Data Flow), Cấu trúc Database, API Contract, UI/UX Mockup, và các kịch bản ngoại lệ/dị thường (Edge Cases/Error Handling).
  - **Spec & Planning (SOP)**: AI/Dev phải tham chiếu luồng `.agent-skills/.gemini/commands/spec.toml` (để lấy yêu cầu/vẽ spec) và `.agent-skills/.gemini/commands/planning.toml` (để phân rã task WBS/nghiệm thu) trong quá trình lập kế hoạch.
  3. **Đối chiếu chéo (Cross-Audit)**: Trước khi chốt Giai đoạn Thiết kế (Phase 1) để chuyển sang Giai đoạn Viết mã (Phase 2), bắt buộc phải thực hiện đối chiếu chéo 1:1. Mỗi "Yêu cầu cốt lõi" phải có ít nhất một task tương ứng trong WBS. Bắt buộc lập "Báo cáo Đối chiếu chéo" dạng bảng lưu trực tiếp vào tệp `PLAN.md` làm bằng chứng nghiệm thu thiết kế.
  4. **Lập Lộ trình thi công (Execution Roadmap)**: Sau khi đã hoàn tất Phase 1 (Thiết kế) và Phase 2 (WBS chi tiết), bắt buộc phải lập "Lộ trình thi công (TDD Execution Sequence)". Lộ trình này phải tuân thủ nghiêm ngặt phương pháp "Outside-In TDD" (Phát triển từ ngoài vào trong: Giao thức/UI -> Lõi nghiệp vụ -> Lưu trữ) để đảm bảo sản phẩm luôn bám sát trải nghiệm người dùng.
  5. **Quy tắc Zero-Bug (Thiết kế Phòng thủ Tuyệt đối)**: Bắt buộc áp dụng nguyên lý: *"Đào sâu, khoét vào từng điểm, bẻ gãy mọi rủi ro trên bản vẽ trước khi gõ bất kỳ dòng code nào"*. Trước khi code bất kỳ module nào, AI phải trình bày Báo cáo Phân tích Rủi ro (Tràn RAM, Bẫy trạng thái, Deadlock, Dữ liệu bẩn) và chờ Chủ nhà "Chốt phương án" (Sign-off) mới được phép thi công.
  6. **Nguyên tắc Linh động & Quản trị Tường minh (Flexibility & Visibility)**: Mọi giá trị mặc định (Default/Static values), các tham số ngoại lệ, hoặc logic rẽ nhánh phải được bóc tách khỏi mã nguồn cứng (hardcode) và đưa ra giao diện cấu hình (UI/JSON) để người dùng có thể chủ động quản lý. Thiết lập ở cấp độ nào (Global/Unit/File) thì phải có không gian quản lý hiển thị rõ ràng riêng biệt ở cấp độ đó.

- **Giao tiếp và Chốt Yêu Cầu (Chủ nhà & Kỹ sư trưởng)**:
  1. **Vai trò**: AI đóng vai "Kỹ sư trưởng" (Lead Engineer), người dùng là "Chủ nhà" (Product Owner - đưa ra ý tưởng bằng ngôn ngữ đời thường).
  2. **Quy trình 3 bước bắt buộc**:
     - *Bước 1 (Khảo sát)*: Phân tích yêu cầu. Nếu mơ hồ, đặt tối đa 5 câu hỏi (ưu tiên dạng trắc nghiệm/ngắn gọn) để làm rõ bối cảnh.
     - *Bước 2 (Lập kế hoạch)*: Trình bày phương án (sửa file nào, thêm logic gì) bằng ngôn ngữ đơn giản. Bắt buộc kết thúc bằng việc xin xác nhận duyệt kế hoạch từ người dùng.
     - *Bước 3 (Thi công)*: Tuyệt đối **KHÔNG** được sinh ra mã nguồn (code) cho đến khi người dùng đã xác nhận "Đồng ý" với kế hoạch ở Bước 2.

## 1. Code Style & Convention
- **Language / Ngôn ngữ**: Python 3.x
- **Naming rules / Quy tắc đặt tên**:
  - **100% English / Bắt buộc tiếng Anh**: Tên biến, hàm, lớp và hằng số phải được đặt tên hoàn toàn bằng tiếng Anh có nghĩa (VD: `get_user_info` thay vì `lay_thong_tin_user`).
  - Variables & functions / Biến & hàm → `snake_case`
  - Classes / Lớp → `PascalCase`
  - Constants / Hằng số → `UPPER_CASE`
- **Imports / Thư viện**:
  - Standard libraries trước, third-party sau, local cuối cùng.
  - Dùng absolute import thay vì relative nếu có thể.
- **Type hints / Kiểu dữ liệu**:
  - Luôn khai báo type hints cho input/output.
  - Ví dụ:

```python
def calculate_area(radius: float) -> float:
    """
    EN: Calculate the area of a circle given its radius.
    VI: Tính diện tích hình tròn dựa trên bán kính.
    """
    return 3.14159 * radius * radius
```

- **Comments / Ghi chú**:
  - Dùng docstring cho module, class, function.
  - Bắt buộc viết comment/docstring song ngữ (EN + VI) ngắn gọn, rõ ràng.
  - Inline comment chỉ khi cần giải thích logic phức tạp.
- **Formatting / Định dạng**:
  - Theo chuẩn PEP8.
  - Dùng Black để auto-format (indent = 4 spaces).
  - Max line length = 88 ký tự.
  - **JSON Format**: Indent = 4 spaces, bắt buộc lưu encoding `UTF-8` (không escape ký tự Unicode). Naming convention cho JSON keys phải đồng nhất (ưu tiên `snake_case`).
- **Error handling / Xử lý lỗi**:
  - Luôn dùng `try/except` rõ ràng, không bắt lỗi chung chung (`except Exception`).
  - Comment giải thích lý do bắt lỗi.
  - **Custom Exceptions**: Bắt buộc tạo thư mục `exceptions/` (bên trong `src/`) để định nghĩa và chứa các lớp ngoại lệ tự tạo (Custom Exceptions). Tuyệt đối không nhồi nhét định nghĩa exception vào các file logic chính.
  - **Retry Mechanism / Cơ chế thử lại**: Bắt buộc áp dụng cơ chế Retry (thử lại khi thất bại) cho tất cả các hàm liên quan đến I/O (Network, Database, File) hoặc gọi API của bên thứ 3 nhằm đảm bảo tính ổn định khi gặp sự cố kết nối hoặc lỗi tạm thời (Transient Errors).

---

## 2. Project Structure
- Thư mục `src/` chứa toàn bộ logic chính.
- Thư mục `logs/` chứa các file nhật ký của ứng dụng (application logs, error logs).
- Thư mục `output/` chứa kết quả xuất ra của chương trình (ví dụ: file CSV, Excel báo cáo).
- Thư mục `data/` (hoặc `database/`) chứa các file CSDL cục bộ, file cấu hình gốc (ví dụ: `master_configs.json`, SQLite).
- **Frontend / Web Assets (Nếu dự án có giao diện Web)**:
  - Thư mục `static/` hoặc `public/` chứa tài nguyên tĩnh (images, css, js).
  - Thư mục `templates/` chứa các file giao diện HTML (nếu dùng Server-Side Rendering).
  - Nếu dùng framework Frontend độc lập (React/Vue/Angular), tách toàn bộ vào thư mục `frontend/` ở root.
- **Multi-module/Monorepo (Dự án lớn gồm nhiều chức năng/dự án nhỏ)**:
  - Tổ chức các chức năng/dự án nhỏ vào thư mục `apps/` hoặc `modules/` (ví dụ: `apps/module_a/`, `apps/module_b/`).
  - Mỗi dự án nhỏ bên trong phải tuân thủ chính xác cấu trúc thư mục độc lập (tự chứa `src/`, `tests/`,...).
  - Các utils, thư viện cốt lõi dùng chung cho nhiều dự án nhỏ nên đặt trong một thư mục `shared/` hoặc `core/` ở root.
- Không để file vượt quá **500 dòng** (ngoại trừ các file PLAN.md, PROJECT_PLAN.md, README.md, AI_RULES.md).
- Bên trong `src/`:
  - `models/` → định nghĩa dữ liệu, class, schema.
  - `services/` → xử lý nghiệp vụ, API call.
  - `utils/` → hàm tiện ích.
  - `controllers/` hoặc `views/` → xử lý request/response (nếu là web app).
  - `config/` → chứa các file thiết lập cấu hình ứng dụng.
- File Python đặt tên theo `snake_case.py`.
- **Quy chuẩn Đặt tên khi Tách File (Semantic Naming)**: Khi một file phình to và cần chia tách, tuyệt đối KHÔNG đặt tên chắp vá làm mất bối cảnh. Bắt buộc giữ nguyên cấu trúc thư mục phẳng hiện tại nhưng áp dụng công thức **[Tiền tố Miền nghiệp vụ]_[Tên chức năng]_[Hậu tố Vai trò].py** để các file cùng nghiệp vụ luôn đứng cạnh nhau theo bảng chữ cái.
  - *Tiền tố (Domain)*: `class_`, `student_`, `accounting_`...
  - *Hậu tố (Role)*: `_view.py` (Màn hình chính), `_tab.py` (Thẻ con), `_widget.py` (Thành phần UI), `_dialog.py` (Cửa sổ nổi).
  - *Ví dụ chuẩn*: `class_tab_planning.py`, `class_widget_links.py`.
- **Code Refactoring & Simplification (SOP)**: Khi cần tối ưu hóa, dọn dẹp mã nguồn hoặc chia tách file lớn, AI phải kích hoạt luồng làm việc tại `.agent-skills/.gemini/commands/refactor.toml`. Nếu chỉ cần đơn giản hóa logic nội bộ, dùng `.agent-skills/.gemini/commands/code-simplify.toml`.
- Thư mục `tests/` chứa unit test, file test đặt tên `test_<module>.py` tương ứng với file trong `src/`.

---

## 3. Flow & Architecture / Luồng & Kiến trúc
- **Development Workflow / Quy trình phát triển**:
  - **Bắt buộc thiết kế GUI (Giao diện người dùng) trước** khi bắt đầu code logic.
  - Khi phân tích dự án, AI/Dev phải phân tích dựa trên trải nghiệm/luồng UI (Mockup/Wireframe) để hiểu rõ mục tiêu, từ đó mới thiết kế Model, Service và Database tương ứng.
- **Layer separation / Phân tầng**:
  - Controller → Service → Model → Database.
  - Không gọi API trực tiếp trong UI hoặc controller, phải qua service.
- **Data flow / Luồng dữ liệu**:
  - Input → Validation → Business logic → Output.
  - Luôn validate dữ liệu trước khi xử lý.
- **Dependency management / Quản lý phụ thuộc**:
  - Dùng `requirements.txt` hoặc `pyproject.toml`.
  - Không hardcode version, dùng range hợp lý.
  - **Bắt buộc cập nhật (Auto-update dependencies)**: Bất cứ khi nào cài đặt hoặc import thêm một thư viện mới của bên thứ 3 vào mã nguồn, AI bắt buộc phải chủ động thêm thư viện đó (kèm theo phiên bản hoặc range hợp lý) vào file `requirements.txt` để đảm bảo dự án luôn chạy được trên môi trường mới.

---

## 4. Security & Performance
- **Security / Bảo mật**:
  - Không hardcode secret, dùng `.env` hoặc secret manager.
  - Luôn sanitize input để tránh SQL injection, XSS.
  - Không dùng `eval()` hoặc `exec()` trừ khi thật cần thiết.
- **Performance / Hiệu năng**:
  - Ưu tiên async/await cho I/O.
  - Tránh vòng lặp lồng nhau quá sâu.
  - Dùng caching khi cần.
- **Logging / Nhật ký**:
  - Dùng `logging` module thay vì `print`.
  - Log phải có level (INFO, WARNING, ERROR).

---

## 5. Testing & CI/CD
- **Testing / Kiểm thử**:
  - Dùng pytest.
  - **Bắt buộc**: Bất kỳ module hoặc function nào mới được tạo ra đều phải đi kèm với unit test tương ứng.
  - **Centralized Testing (Kiểm thử Tập trung - Cấu trúc Phẳng)**: Tuyệt đối KHÔNG đặt các file `test_*.py` nằm rải rác. BẮT BUỘC 100% các file test phải được lưu tập trung và đặt TRỰC TIẾP (cấu trúc phẳng) ngay bên trong thư mục `tests/` ở root dự án. KHÔNG tạo thêm các thư mục con bên trong `tests/` để dễ dàng quản lý và tránh rắc rối (VD: `tests/test_i18n_manager.py`).
  - **TDD linh hoạt**: Bắt buộc áp dụng TDD (Viết test trước, code sau) cho lớp Lõi nghiệp vụ (Services, Utils, Models). Riêng đối với lớp Giao diện (UI/Views), cho phép vẽ Code UI trước để chốt trải nghiệm, sau đó viết Unit Test ngay sau đó.
  - **Prove-It Pattern (SOP)**: Khi bắt đầu phát triển tính năng mới hoặc vá lỗi (Bug Fix), AI/Kỹ sư bắt buộc phải kích hoạt quy trình tại `.agent-skills/.gemini/commands/test.toml` để tuân thủ luồng TDD (viết test thất bại trước -> sửa code -> test pass).
  - Không chấp nhận code logic (Service, Utils, Model) mà không có test.
  - Coverage tổng thể và cho từng file tối thiểu ≥ 80%.
  - **Bắt buộc chạy test (Auto-run tests)**: Ngay sau khi hoàn thành việc viết code cho một tính năng (feature), AI phải cung cấp sẵn lệnh shell (ví dụ: `pytest`) và yêu cầu người dùng (Chủ nhà) chạy thử, sau đó chờ nhận kết quả (Log) để xác nhận code hoạt động chính xác trước khi chuyển sang bước tiếp theo.
- **CI/CD / Tích hợp liên tục**:
  - Pipeline chạy lint + test trước khi merge.
  - Reject commit nếu vi phạm rule.
- **Example test / Ví dụ kiểm thử**:

```python
def test_calculate_area():
    """
    EN: Test circle area calculation with radius = 2.
    VI: Kiểm thử tính diện tích hình tròn với bán kính = 2.
    """
    assert calculate_area(2) == 12.56636
```

---

## 6. Documentation
- Mỗi module phải có README ngắn mô tả chức năng.
- Cập nhật tài liệu kiến trúc (nếu có) khi thêm module/flow mới.
- **Bảo toàn tài liệu (Content Preservation)**: Khi cập nhật tự động nội dung kiến trúc vào `README.md` (hoặc các file tài liệu khác), AI **bắt buộc** phải dựa vào các cờ đánh dấu (markers) như `<!-- ARCHITECTURE_START -->` và `<!-- ARCHITECTURE_END -->` để chỉ thay thế đúng phần nội dung ở giữa. Tuyệt đối không được ghi đè toàn bộ file làm mất các đoạn văn bản giải thích do người dùng tự viết.
- **Documentation Workflow (SOP)**: Khi viết docstring, sinh tài liệu README hoặc comment giải thích logic, AI cần tham chiếu quy trình tại `.agent-skills/.gemini/commands/document.toml`.
- Tài liệu API (Swagger/Postman hoặc file Markdown) phải luôn được cập nhật đồng bộ với code.

---

## 7. Git & Version Control
- **Commit Message Convention / Chuẩn commit**:
  - Tuân thủ nghiêm ngặt [Conventional Commits](https://www.conventionalcommits.org/).
  - Cấu trúc: `<type>(<scope>): <subject>`
  - Các `type` bắt buộc: `feat` (tính năng mới), `fix` (sửa lỗi), `docs` (tài liệu), `style` (format, không đổi logic), `refactor` (tối ưu code), `test` (kiểm thử), `chore` (cấu hình, tool, build).
  - Tiêu đề (subject) ngắn gọn, **không quá 72 ký tự**, viết rõ ràng (có thể dùng EN/VI nhưng phải thống nhất).
- **Branch Naming / Đặt tên nhánh**:
  - `feature/<tên-chức-năng>` (ví dụ: `feature/export-excel`)
  - `bugfix/<tên-lỗi>` (ví dụ: `bugfix/fix-null-pointer`)
  - `hotfix/<tên-lỗi-nghiêm-trọng>` cho các bản vá khẩn cấp cần đưa lên production ngay.
- **Incremental Implementation (SOP)**: Trong quá trình phát triển, AI phải áp dụng vòng lặp phát triển tăng dần được quy định tại `.agent-skills/.gemini/commands/build.toml`. Tuyệt đối không nhảy cóc qua bước chạy Test và Build trước khi Commit.
- **Pull Request / Merge Request**:
  - PR phải có mô tả rõ ràng (What, Why, How).
  - Khuyến khích squash các commit "rác" (như "fix typo", "update again") thành 1 commit có ý nghĩa trước khi merge.
  - **5-Axis Code Review (SOP)**: Trước khi chốt mã nguồn hoặc tạo PR, AI bắt buộc phải tự review lại code dựa trên 5 trục tiêu chuẩn được định nghĩa tại `.agent-skills/.gemini/commands/review.toml`, sau đó phân loại cảnh báo theo mức độ.

---

## 8. Build & Packaging / Đóng gói ứng dụng
- **Module Recognition / Nhận diện Module**:
  - Bắt buộc: Mọi thư mục chứa mã nguồn Python (như `src/`, `views/`, `services/`...) đều phải chứa file `__init__.py` (kể cả file trống). Điều này giúp Python và các công cụ đóng gói (PyInstaller) nhận diện chính xác đó là một Package hợp lệ.
- **Path Resolution / Cấu hình Đường dẫn**:
  - Không lạm dụng hoặc phụ thuộc hoàn toàn vào biến `__file__` để lấy đường dẫn gốc. Khi ứng dụng được đóng gói thành file thực thi (ví dụ: `.exe`), `__file__` sẽ không còn trỏ đúng cấu trúc thư mục vật lý.
  - Đối với các file tài nguyên tĩnh (assets, configs, templates), luôn sử dụng cơ chế kiểm tra môi trường linh hoạt (VD: kiểm tra `getattr(sys, 'frozen', False)` để lấy `sys._MEIPASS` cho PyInstaller).
  - **Xử lý tệp tĩnh (Static Assets)**: Đối với các tệp tĩnh (ảnh, icon, configs), tuyệt đối KHÔNG gọi trực tiếp bằng đường dẫn tương đối (VD: `open("assets/icon.png")`). Luôn dùng `os.path.join(project_root, "assets", "icon.png")` với `project_root` đã được phân giải an toàn qua cơ chế `sys._MEIPASS`.
- **System Path Manipulation / Can thiệp sys.path**:
  - **Tuyệt đối KHÔNG sử dụng `sys.path.insert(0, ...)` hoặc `sys.path.append(...)` để hack đường dẫn import.** Hành động này phá vỡ cơ chế resolve module mặc định của Python và PyInstaller, là nguyên nhân chính gây ra lỗi `ModuleNotFoundError: No module named 'src'`.
- **Execution Context / Ngữ cảnh thực thi (Tránh lỗi Not module src)**:
  - **Bắt buộc**: Các file Entry Point (như `main.py`, `app.py`, `gui_init_project.py`) phải luôn được đặt ở **thư mục gốc (root)** của dự án.
  - Khi build PyInstaller, **chỉ** được truyền vào file Entry Point ở root (VD: `pyinstaller gui_init_project.py`), tuyệt đối không truyền file nằm trong `src/`.
  - Khi test/run code thủ công, nếu cần chạy một file sâu bên trong `src/`, phải đứng ở thư mục gốc và dùng cờ `-m` (VD: `python -m src.views.main_window`). Tuyệt đối KHÔNG chạy trực tiếp `python src/views/main_window.py`.
- **Build Configuration / Cấu hình đóng gói**:
  - **Bắt buộc**: Phải luôn tạo một kịch bản đóng gói chuyên dụng (ví dụ: `build.py`, `Makefile`, hoặc file `.spec` của PyInstaller) để quản lý quá trình build thay vì gõ lệnh CLI thủ công.
  - **Bảo trì và Đồng bộ**: Tệp kịch bản đóng gói này phải luôn được kiểm tra và cập nhật đồng bộ ngay lập tức mỗi khi có thay đổi trong mã nguồn ảnh hưởng đến quá trình đóng gói (ví dụ: thêm tệp tài nguyên tĩnh `assets`, bổ sung thư viện phụ thuộc ẩn, hoặc thay đổi tên Entry Point).
  - **Clean Build / Dọn dẹp trước khi đóng gói**: Trước khi thực thi lệnh PyInstaller, kịch bản build bắt buộc phải quét và xóa sạch các tệp/thư mục tạm (như `__pycache__`, thư mục `build/`, `dist/`, hoặc các file `.log` cũ) để đảm bảo tệp thực thi luôn là phiên bản tinh gọn nhất và không bị đóng gói nhầm mã nguồn cũ.
- **Pre-launch Checklist (SOP)**: Trước khi chốt release bản build cuối cùng, AI bắt buộc phải kích hoạt luồng đánh giá đa trục tại `.agent-skills/.gemini/commands/ship.toml` để tổng hợp báo cáo Review, Security, Test Coverage và chốt quyết định GO/NO-GO.

---

## 9. Copyright & Licensing / Bản quyền & Giấy phép
- **License File**: Bất kỳ dự án hoặc module mã nguồn mở nào được khởi tạo cũng phải đi kèm một tệp giấy phép rõ ràng ở thư mục gốc.
- **Copyright Header**: Đối với các dự án nội bộ doanh nghiệp hoặc dự án thương mại, các file mã nguồn quan trọng nên có một đoạn chú thích bản quyền ở phần đầu của file.
- **Tuân thủ Dependency**: Khi sử dụng thư viện bên thứ 3 (trong `requirements.txt`), phải đảm bảo quy định sử dụng của chúng không xung đột với định hướng của dự án gốc.

---

## 10. Blood Rules / Nguyên tắc xương máu từ thực tiễn
Những nguyên tắc này được đúc kết từ các sự cố nghiêm trọng (treo máy, sập luồng, phình to kiến trúc) trong quá trình phát triển thực tế, bắt buộc AI/Dev phải kiểm tra trước khi viết code:

- **Xử lý I/O Phòng thủ & Kiểm thử Dữ liệu Bẩn (Defensive I/O & Dirty Testing)**: 
  - *Nguyên tắc*: Không bao giờ tin tưởng tuyệt đối vào ranh giới dữ liệu do thư viện bên thứ 3 báo cáo (VD: `openpyxl.max_row` có thể lên tới 1 triệu dòng do lỗi format của người dùng). Bắt buộc phải tự viết các cơ chế "Cắt tỉa" (Trim) hoặc "Ngắt tự động" (Break - ngắt sau 50 dòng/20 cột trống). 
  - *Kiểm thử*: Các bài Unit Test cho Service xử lý dữ liệu bắt buộc phải có kịch bản test "Dữ liệu rác" để kiểm chứng khả năng chịu đựng của hệ thống.
- **Tối ưu hóa Cập nhật UI Hàng loạt (Bulk Update Optimization)**: 
  - *Nguyên tắc*: Khi thêm/xóa/sửa số lượng lớn phần tử trên giao diện (`QTableWidget`, `QListWidget`), **bắt buộc** phải khóa luồng render (`setUpdatesEnabled(False)`), dọn dẹp bộ nhớ đệm (`setRowCount(0)`), bơm dữ liệu, sau đó mới mở khóa render. Điều này ngăn chặn lỗi "ngạt thở" UI do tính năng tự động co giãn (`ResizeToContents`) bị kích hoạt hàng triệu phép tính thừa.
- **Ranh giới Nghiệp vụ Nghiêm ngặt (Strict Domain Boundaries)**: 
  - *Nguyên tắc*: Tuyệt đối tuân thủ Kiến trúc Phân tầng. Không được phép nhồi nhét UI hoặc Logic của module này (VD: Làm giàu dữ liệu Sinh viên) vào bên trong module khác (VD: Quản lý Lớp học). Nếu một tệp vượt quá 500 dòng, bắt buộc dừng lại để chia tách (Refactor).
- **Rải bẫy Đo lường Hiệu năng (Performance Trapping)**: 
  - *Nguyên tắc*: Đối với các tác vụ "nặng đô" (như đọc/ghi Excel lớn, gọi API), bắt buộc phải chèn các hàm ghi log thời gian thực (timestamps) tại các điểm nút (Milestones). Đề phòng trường hợp ứng dụng "chết lâm sàng" không văng Exception (Silent Crash), dòng log cuối cùng sẽ ngay lập tức chỉ điểm rò rỉ hiệu năng.
- **Debugging & Troubleshooting (SOP)**: Khi ứng dụng gặp sự cố (Crash, Bug logic, Rò rỉ bộ nhớ), AI phải tuân thủ luồng khoanh vùng và phân tích lỗi được định nghĩa tại `.agent-skills/.gemini/commands/debug.toml`.
- **Giới hạn của E2E Test & Rủi ro từ Batch Script (Testing Boundaries & Batch Traps)**:
  - *Nguyên tắc*: Ngôn ngữ Batch (`.bat`) của Windows cực kỳ lỏng lẻo, rất dễ dính bẫy cú pháp (lỗi lồng khối `()`, lỗi `Delayed Expansion`). Tuyệt đối hạn chế viết logic rẽ nhánh phức tạp, gọi API bằng `.bat`. Ưu tiên dùng Python (`.py`) cho các kịch bản tự động hóa để tận dụng khả năng Unit Test. Nếu bắt buộc dùng `.bat`, hãy chia nhỏ bằng `goto` thay vì lồng khối quá sâu.
  - *Kiểm thử*: Cảnh giác với "Điểm mù E2E": Hệ thống test E2E báo PASS khi file `.bat` được tạo ra trên ổ cứng KHÔNG đồng nghĩa với việc script đó chạy đúng. Các script tương tác với hạ tầng (Git, GitHub CLI, PyInstaller) bắt buộc phải có bước nghiệm thu thủ công (Manual QA) chạy thử thực tế cục bộ, không được tin tưởng mù quáng vào kết quả của test tự động tĩnh.
- **Điểm mù E2E trong Xử lý Dữ liệu & Báo cáo (E2E Data Assertion)**:
  - *Nguyên tắc*: Báo cáo PASS của E2E Test khi "chạy không văng lỗi" và "file xuất ra ổ cứng thành công" là một Ảo giác kiểm thử (Testing Illusion). Hệ thống test tĩnh không tự biết nội dung dữ liệu bên trong bị lệch dòng hay ghi đè.
  - *Kiểm thử*: Đối với các luồng tổng hợp dữ liệu, xuất báo cáo (Excel, CSV), bài test E2E **bắt buộc phải có Data Assertion (Khẳng định Dữ liệu)**. Bài test phải mở file kết quả, đọc tọa độ cụ thể và assert tính chính xác (VD: Dữ liệu file A phải tiếp nối file B, tổng số dòng output phải bằng tổng các file input). Các logic nội tại như "tìm dòng trống tiếp theo" bắt buộc phải được tách thành hàm Pure Function và bảo vệ bằng Unit Test với các kịch bản chứa dữ liệu rác (Ghost Rows).

---

## 11. AI Output Generation & Diff Discipline / Kỷ luật sinh mã và vá lỗi
Để tránh các lỗi khi áp dụng mã nguồn (patching/merging) do IDE từ chối hoặc bị tràn giới hạn token, AI bắt buộc tuân thủ:

- **Chấp nhận viết tắt có kiểm soát trong Diff (Controlled Elision)**: Cho phép sử dụng `...` hoặc `# ... (giữ nguyên code cũ) ...` trong các khối mã `diff` nếu khoảng cách giữa hai điểm cần sửa chữa trong cùng một file quá lớn.
- **Sao chép nguyên trạng bối cảnh (Exact Context Matching)**: Các dòng code không thay đổi (context lines) và các dòng bị xóa (bắt đầu bằng dấu `-`) phải được sao chép **chính xác 100%** từ file gốc (bao gồm cả thụt lề, khoảng trắng). Không tự ý sửa lỗi chính tả hay định dạng ở các dòng bối cảnh này.
- **Gộp khối vá (Single Diff Block per File)**: Nếu cần thay đổi nhiều vị trí trong cùng một tệp, bắt buộc phải gộp chúng vào **một khối `diff` duy nhất** (sử dụng nhiều phần `@@ ... @@` hoặc dùng `...` để rút gọn khoảng giữa), tuyệt đối không tách ra thành nhiều khối diff riêng biệt cho cùng một tệp.
- **Phân rã Output (Output Chunking)**: Nếu một tính năng yêu cầu tạo mới/sửa đổi từ 3 file trở lên, HOẶC tổng số dòng code thay đổi vượt quá 150 dòng, AI **tuyệt đối không được nhồi nhét tất cả vào một lần trả lời**. Phải chủ động chia nhỏ việc giao code thành nhiều đợt (Ví dụ: *"Phần 1: Models & Utils. Lưu lại và gõ 'Tiếp' để nhận Phần 2"*).
- **Giới hạn bối cảnh (Strict Context Limit)**: Khi sử dụng chuẩn `diff`, chỉ được in ra tối đa **3 đến 5 dòng code cũ (context lines)** ở trên và dưới đoạn mã cần sửa. Tuyệt đối không in lại toàn bộ các hàm không liên quan hoặc cả một file dài chỉ để sửa một vài chỗ, nhằm tiết kiệm bộ nhớ output token.

---

## 12. Documentation Synchronization (Đồng bộ tài liệu Blueprint)
- **Mục tiêu**: `MASTER_BLUEPRINT.md` đóng vai trò là "Bộ não trung tâm" của dự án, lưu trữ toàn diện tư duy thiết kế, các quyết định kỹ thuật, và lịch sử tiến hóa của dự án.
- **Quy tắc Ánh xạ thông tin (Mapping Rules)**:
    1. **Định danh nguồn (Source Tagging)**: Mọi nội dung thảo luận trong `PLAN.md` phải được AI ghi nhận kèm theo một định danh duy nhất (Tag) phù hợp với ngữ cảnh hiện tại. AI chỉ sử dụng một trong ba loại Tag sau: `[PHASE: X]`, `[STATION: Y]`, hoặc `[STEP: Z]`.
    2. **Cập nhật theo cấu trúc cây (Tree-based Update)**: AI tuyệt đối không được đổ dồn thông tin. Thông tin phải được ánh xạ vào đúng vị trí trong `MASTER_BLUEPRINT.md` theo phân cấp tương ứng với định danh đã chọn (Phase, Station, hoặc Step).
    3. **Tính kế thừa (Inheritance & Cross-Reference)**: Nếu một quyết định tại định danh hiện tại làm thay đổi logic của các phần khác, AI bắt buộc phải cập nhật mục `Change Log` và sử dụng tag `[CROSS-REFERENCE]` để kết nối các thông tin liên quan, đảm bảo tính nhất quán của hệ thống.
- **Quy tắc trích xuất nội dung (Extraction Rules)**:
    1. **Chi tiết hóa tuyệt đối**: Cấm ghi vắn tắt. Mọi phân tích kỹ thuật, lựa chọn giải pháp (tại sao chọn A thay vì B), và các kịch bản ngoại lệ (Edge Cases) phải được giải trình chi tiết.
    2. **Nội dung bắt buộc trong Blueprint**:
        - `## 1. Tổng quan & Mục tiêu`
        - `## 2. Kiến trúc & Phân tích kỹ thuật (Technical Depth - Theo định danh Phase/Station/Step tương ứng)`
        - `## 3. Các quyết định thiết kế (Design Decisions - Lý giải tại sao?)`
        - `## 4. Các tình huống & Kịch bản (Scenarios & Edge Cases)`
        - `## 5. Lưu ý vận hành (Operations & Constraints)`
        - `## 6. Nhật ký thay đổi (Change Log & Cross-References)`
- **Quy trình Chốt phiên (Session Closing)**:
    1. Cuối mỗi phiên làm việc, AI bắt buộc phải chủ động tổng hợp dữ liệu từ `PLAN.md` và thực hiện cập nhật vào `MASTER_BLUEPRINT.md` dựa trên cấu trúc đã định danh.
    2. Nếu có phát sinh mới, AI phải đề xuất bổ sung mục hoặc chèn vào vị trí logic nhất, đảm bảo `MASTER_BLUEPRINT.md` là "Living Documentation".
- **Lệnh thực thi**: Người dùng có thể ra lệnh "Cập nhật Blueprint" bất cứ lúc nào, AI phải thực h iện rà soát và đồng bộ hóa dựa trên lịch sử hội thoại gần nhất.

---

## 13. Agent Skills Delegation (Sổ tay Quy trình Thực thi)
- **Định hướng**: Mọi quy trình thực thi chi tiết (Workflows/SOPs) của AI Agent được quản lý tập trung tại thư mục `.agent-skills/.gemini/commands/`. `AI_RULES.md` đóng vai trò "Hiến pháp" định hướng, các file `.toml` là cẩm nang hướng dẫn hành động cụ thể.
- **Danh mục Skills (Con trỏ)**:
    1. **`test.toml` (TDD & Prove-It)**: Sử dụng khi vá lỗi hoặc làm tính năng mới để đảm bảo có test case thất bại trước khi viết code.
    2. **`build.toml` (Incremental Implementation)**: Sử dụng để chạy vòng lặp thi công tăng dần (Test -> Code -> Verify -> Commit).
    3. **`review.toml` (5-Axis Review)**: Sử dụng trước khi chốt tính năng để quét mã nguồn trên 5 trục: Correctness, Readability, Architecture, Security, Performance.
    4. **`document.toml` (Documentation)**: Sử dụng để sinh docstring, viết tài liệu README, API docs chuẩn mực.
    5. **`refactor.toml` (Code Refactoring)**: Sử dụng khi cần tối ưu hóa, dọn dẹp mã nguồn, hoặc chia tách các file vượt quá 500 dòng.
    6. **`debug.toml` (Debugging & Fixes)**: Sử dụng để phân tích nguyên nhân gốc rễ (Root Cause Analysis) và vá các lỗi phức tạp trong hệ thống.
    7. **`spec.toml` (Spec-Driven)**: Sử dụng ở Phase 1 để lấy yêu cầu, định nghĩa phạm vi, cấu trúc và ranh giới hệ thống trước khi gõ code.
    8. **`planning.toml` (Task Breakdown)**: Sử dụng để phân rã spec thành các task nhỏ (WBS) có Acceptance Criteria để thi công.
    9. **`code-simplify.toml` (Code Simplification)**: Sử dụng để đơn giản hóa logic, giảm độ phức tạp của hàm/lớp mà không thay đổi hành vi.
    10. **`ship.toml` (Shipping & Pre-launch)**: Trình quản lý đa đặc vụ (Orchestrator) chạy các bài kiểm tra song song (Code Review, Security, Test) để chốt quyết định Release.