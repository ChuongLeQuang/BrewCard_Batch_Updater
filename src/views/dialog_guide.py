"""
EN: Dialog showing comprehensive user guide and formula syntax.
VI: Hộp thoại hiển thị hướng dẫn sử dụng chi tiết và cú pháp công thức.
"""

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QTextBrowser,
    QApplication,
    QPushButton,
    QWidget,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette


class GuideDialog(QDialog):
    """
    EN: Dialog showing comprehensive user guide and formula syntax.
    VI: Hộp thoại hiển thị hướng dẫn sử dụng chi tiết và cú pháp công thức.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("📖 Hướng dẫn Sử dụng & Cú pháp Công thức")
        self.resize(820, 680)
        self.setWindowFlags(
            self.windowFlags()
            | Qt.WindowType.WindowMinMaxButtonsHint
            | Qt.WindowType.Window
        )
        layout = QVBoxLayout(self)

        browser = QTextBrowser(self)
        browser.setOpenExternalLinks(True)

        is_dark = False
        app = QApplication.instance()
        if app:
            window_color = app.palette().color(QPalette.ColorRole.Window)
            is_dark = window_color.lightness() < 128

        if is_dark:
            text_color = "#e0e0e0"
            border_color = "#444"
            th_bg_color = "#3d3d3d"
            code_bg_color = "#3a3a3a"
            code_text_color = "#66d9ef"
            main_header_bg = "#212121"
            main_header_color = "#2a82da"

            box_info_bg = "rgba(42, 130, 218, 0.15)"
            box_info_border = "#2a82da"
            box_success_bg = "rgba(40, 167, 69, 0.15)"
            box_success_border = "#28a745"
            box_warning_bg = "rgba(230, 126, 34, 0.15)"
            box_warning_border = "#e67e22"
            box_error_bg = "rgba(220, 53, 69, 0.15)"
            box_error_border = "#dc3545"
        else:
            text_color = "#2c3e50"
            border_color = "#dcdde1"
            th_bg_color = "#f5f6fa"
            code_bg_color = "#f1f2f6"
            code_text_color = "#0097e6"
            main_header_bg = "#333333"
            main_header_color = "white"

            box_info_bg = "#e8f4fd"
            box_info_border = "#2a82da"
            box_success_bg = "#edf7ed"
            box_success_border = "#28a745"
            box_warning_bg = "#fff4e5"
            box_warning_border = "#e67e22"
            box_error_bg = "#fde8e8"
            box_error_border = "#dc3545"

        html_content = f"""
        <div style='font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; font-size: 13px; color: {text_color};'>
            <h1 style='color: #2A82DA; border-bottom: 2px solid #2A82DA; padding-bottom: 5px; font-size: 18px; margin-top: 0;'>📖 CẨM NANG HƯỚNG DẪN SỬ DỤNG CHI TIẾT (TỪ A ĐẾN Z)</h1>
            
            <p>Hệ thống hỗ trợ tự động hóa việc đọc, kiểm tra chất lượng (QC) và gộp dữ liệu mẻ nấu bia (BrewCard) từ các file Excel đơn lẻ của nhà nấu vào một file <b>Master (Tổng hợp)</b> duy nhất. Dưới đây là hướng dẫn cụ thể từng bước thực hiện dành cho người dùng mới:</p>

            <!-- HỘP THÔNG TIN CẢNH BÁO BẢO VỆ DỮ LIỆU -->
            <div style='background-color: {box_success_bg}; border-left: 4px solid {box_success_border}; padding: 12px; border-radius: 4px; margin-bottom: 15px;'>
                <b style='color: {box_success_border}; font-size: 14px;'>🛡️ CƠ CHẾ BẢO VỆ DỮ LIỆU & TRÁNH MẤT MÁT (AN TOÀN TUYỆT ĐỐI)</b>
                <ul style='margin-top: 6px; margin-bottom: 0; padding-left: 20px;'>
                    <li><b>Cập nhật tại chỗ (In-place Sync):</b> Phần mềm chỉ ghi đè dữ liệu lên các cột được khai báo ánh xạ (Mapping). Các cột ghi chú tự do bên ngoài bản đồ mapping trên file Master sẽ được <b>giữ nguyên 100%</b>, không bị xáo trộn hay mất dòng.</li>
                    <li><b>Tự động Sao lưu (Auto-Backup):</b> Trước mỗi lần thực hiện ghi dữ liệu, phần mềm tự động sao lưu một bản dự phòng tại thư mục <code>data/backups/</code> có gắn nhãn thời gian (Ví dụ: <code>Master_backup_20260625_173000.xlsx</code>). Bạn hoàn toàn có thể khôi phục lại file gốc bất kỳ lúc nào nếu xảy ra sự cố mất điện hoặc lỗi hệ thống.</li>
                </ul>
            </div>

            <!-- BƯỚC 1 -->
            <div style='background-color: {box_info_bg}; border-left: 4px solid {box_info_border}; padding: 15px; border-radius: 4px; margin-bottom: 15px;'>
                <h3 style='margin: 0 0 10px 0; color: {box_info_border}; font-size: 15px;'>⚙️ BƯỚC 1: THIẾT LẬP CẤU HÌNH ÁNH XẠ (Chỉ làm 1 lần duy nhất)</h3>
                Để phần mềm biết cách trích xuất dữ liệu từ các file con và ghi vào đúng vị trí file Master, bạn thực hiện cấu hình tại Tab <b>"Cấu hình Hệ thống"</b>:
                <ol style='margin-top: 8px; margin-bottom: 0; padding-left: 20px;'>
                    <li style='margin-bottom: 8px;'>
                        <b>Quản lý Hồ sơ (Profiles):</b> Cho phép bạn lưu nhiều bộ cấu hình khác nhau (ví dụ: một profile cho biểu mẫu cũ, một profile cho biểu mẫu mới).
                        <br><i>* Cách tạo mới: Nhập tên profile trực tiếp vào ô ComboBox <b>"Hồ sơ Cấu hình (Profile)"</b> rồi bấm <b>💾 Lưu Cấu Hình</b>.</i>
                    </li>
                    <li style='margin-bottom: 8px;'>
                        <b>Chọn File Đích (Master):</b>
                        <ul>
                            <li>Nhấp nút <code>📁 Chọn tệp</code> để chọn đường dẫn tới file Excel Tổng hợp (Master) của bạn.</li>
                            <li>Chọn hoặc nhập chính xác tên <b>Sheet đích</b> (Ví dụ: <code>BrewSync</code>).</li>
                            <li>Nhập số <b>Dòng tiêu đề</b> (Ví dụ: dòng <code>5</code>). Đây là dòng chứa tên các cột (Số mẻ, Nhiệt độ, Thời gian...). Phần mềm sẽ đọc dòng này để lấy danh sách tên cột đích hiển thị trong bảng Mapping.</li>
                        </ul>
                    </li>
                    <li style='margin-bottom: 8px;'>
                        <b>Tự động nhận diện File Con (Input Files):</b>
                        <ul>
                            <li><b>Tên Sheet lấy dữ liệu:</b> Nhập tên sheet chứa mẻ nấu ở file con (Ví dụ: <code>BrewCard</code>). Nếu file con chứa nhiều sheet cần gom, hãy nhập ngăn cách bằng dấu phẩy (Ví dụ: <code>Mẻ 1, Mẻ 2</code>). Để trống nếu muốn quét tất cả các sheet.</li>
                            <li><b>Dấu hiệu nhận diện (Vân tay) - Cực kỳ quan trọng:</b> Giúp phần mềm nhận biết đúng cấu trúc file, tránh quét nhầm các file nháp hoặc file rác. Cú pháp: <code>Tọa_Độ_Ô=Nội_Dung_Cố_Định</code> (Ví dụ: <code>D3=Order: & G3=Batch:</code>). Phần mềm chỉ đọc file nếu các ô này khớp chính xác nội dung cố định trong file Excel con.</li>
                            <li><b>Hồ sơ dự phòng:</b> Nếu bạn có 2 loại biểu mẫu cũ và mới, hãy tạo 2 Profile riêng biệt. Tại Profile chính, chọn Profile phụ làm "Hồ sơ dự phòng". Khi quét QC, phần mềm sẽ tự động thử cả 2 vân tay để nhận diện tự động.</li>
                        </ul>
                    </li>
                    <li style='margin-bottom: 8px;'>
                        <b>Thiết lập Bản đồ Ánh xạ (Mappings):</b> Click <code>➕ Thêm dòng ánh xạ</code> để tạo liên kết:
                        <ul>
                            <li><b>Cột đích (Chữ cái):</b> Nhập hoặc chọn cột trên file Master (Ví dụ: <code>B</code>). Tên cột đích tương ứng sẽ tự động hiển thị để bạn đối chiếu.</li>
                            <li><b>🔑 Khóa chính:</b> Tích chọn <b>duy nhất 1 dòng</b> đại diện cho Số mẻ (Batch Number). Đây là mã định danh duy nhất để phần mềm nhận diện mẻ nấu và đối chiếu tránh trùng lặp dữ liệu.</li>
                            <li><b>Nguồn dữ liệu / Công thức:</b> Nhập tọa độ ô của file con cần lấy giá trị (Ví dụ: <code>H3</code>) hoặc công thức tính toán động.
                                <br><i>* Mẹo chọn tọa độ nhanh: Nhấp chuột vào ô Nguồn, bấm <code>🎯 Mở Excel ảo chọn Ô</code>, một lưới Excel giả lập trực quan sẽ hiện ra để bạn click chọn ô thay vì gõ tay.</i>
                                <br><i>* Mẹo sắp xếp: Bấm nút <code>🧹 Sắp xếp A-Z</code> để tự động đưa các dòng ánh xạ về đúng thứ tự chữ cái cột (A, B, C... AA, AB) giúp dễ quản lý.</i>
                            </li>
                            <li><b>Định dạng hiển thị:</b> Chọn kiểu hiển thị tương ứng (Số nguyên, Số thập phân, Phần trăm %, Ngày tháng, Giờ phút) để dữ liệu ghi xuống file Master hiển thị chuẩn xác nhất.</li>
                        </ul>
                    </li>
                    <li style='margin-bottom: 8px;'>
                        <b>Nạp Công thức Tự động (Smart Auto-Import):</b> Nếu bạn đã có sẵn một file con chứa công thức ánh xạ, click <code>🔄 Nạp Công thức từ File...</code>:
                        <ul>
                            <li>Chọn file con -> Chọn Sheet và xác định vùng tiêu đề bằng <b>Hộp thoại Chọn cột</b>.</li>
                            <li>Phần mềm sẽ tự động phân tích và tạo bảng Mapping. Nếu tên cột không khớp hoàn toàn, <b>Hộp thoại Ghép nối thủ công (Alias)</b> sẽ hiện ra để bạn xác nhận hoặc bổ sung từ đồng nghĩa (Alias Memory) để hệ thống tự học cho lần sau.</li>
                        </ul>
                    </li>
                    <li>Bấm nút <b>💾 Lưu Cấu Hình</b> ở dưới cùng để ghi nhận các thay đổi.</li>
                </ol>
            </div>

            <!-- BƯỚC 2 -->
            <div style='background-color: {box_warning_bg}; border-left: 4px solid {box_warning_border}; padding: 15px; border-radius: 4px; margin-bottom: 15px;'>
                <h3 style='margin: 0 0 10px 0; color: {box_warning_border}; font-size: 15px;'>📥 BƯỚC 2: KÉO THẢ VÀ KIỂM TRA CHẤT LƯỢNG (QC Check)</h3>
                Chuyển sang Tab <b>"Kiểm tra Chất lượng (QC)"</b> để kiểm định các file con trước khi gộp:
                <ol style='margin-top: 8px; margin-bottom: 0; padding-left: 20px;'>
                    <li style='margin-bottom: 6px;'><b>Nạp file dữ liệu:</b> Chọn các tệp Excel mẻ nấu con (.xlsx, .xlsm) từ máy tính, kéo và thả trực tiếp vào vùng nét đứt màu xám trên giao diện.</li>
                    <li style='margin-bottom: 6px;'><b>Bắt đầu Quét:</b> Nhấp nút <code>🔬 Bắt đầu Quét QC</code>. Hệ thống sẽ xử lý đa luồng chạy ẩn để kiểm tra chi tiết cấu trúc và tính toán công thức của từng tệp.</li>
                    <li style='margin-bottom: 6px;'><b>Theo dõi Trạng thái QC:</b>
                        <ul>
                            <li><span style='color: #28A745; font-weight: bold;'>✅ Đạt (X mẻ):</span> Biểu mẫu chuẩn khớp vân tay, dữ liệu tính toán sạch, sẵn sàng gộp.</li>
                            <li><span style='color: #E67E22; font-weight: bold;'>⚠️ Đạt - Có lỗi:</span> Trích xuất được mẻ nấu nhưng có ô bị lỗi công thức tính toán (Ví dụ: chia cho 0, ô tham chiếu bị trống hoặc sai định dạng). <b>Hãy nhấp đúp vào ô trạng thái để xem chi tiết danh sách ô bị lỗi.</b></li>
                            <li><span style='color: #DC3545; font-weight: bold;'>❌ Lỗi:</span> File sai vân tay (không nhận diện được biểu mẫu), file bị lỗi định dạng, hoặc file đang bị khóa (đang mở trên Excel). Bạn cần đóng Excel hoặc sửa file, sau đó bấm quét lại.</li>
                        </ul>
                    </li>
                    <li><b>Xuất báo cáo QC:</b> Bấm nút <code>📂 Xuất báo cáo QC</code> để xuất file nhật ký lỗi (.txt) gửi cho nhà nấu hoặc bộ phận vận hành sửa chữa file con nếu cần.</li>
                </ol>
            </div>

            <!-- BƯỚC 3 -->
            <div style='background-color: {box_success_bg}; border-left: 4px solid {box_success_border}; padding: 15px; border-radius: 4px; margin-bottom: 20px;'>
                <h3 style='margin: 0 0 10px 0; color: {box_success_border}; font-size: 15px;'>🚀 BƯỚC 3: TỔNG HỢP VÀ GỘP DỮ LIỆU VÀO FILE MASTER</h3>
                Sau khi quét QC xong, chuyển sang Tab <b>"Tổng hợp dữ liệu"</b>:
                <ol style='margin-top: 8px; margin-bottom: 0; padding-left: 20px;'>
                    <li style='margin-bottom: 6px;'><b>Xem trước dữ liệu (Preview):</b> Bảng lưới sẽ hiển thị trước toàn bộ dữ liệu hợp lệ sẽ được ghi vào file Master. Kiểm tra kỹ các giá trị tại đây.</li>
                    <li style='margin-bottom: 6px;'><b>Lưu ý quan trọng trước khi chạy:</b> <span style='color: #FF3333; font-weight: bold;'>Bắt buộc phải đóng file Master trên phần mềm Microsoft Excel.</span> Nếu file đang mở, Windows sẽ khóa quyền ghi (Permission Denied) khiến phần mềm báo lỗi và không thể lưu dữ liệu.</li>
                    <li style='margin-bottom: 6px;'><b>Bắt đầu Tổng hợp:</b> Nhấp nút <code>🚀 Bắt đầu Tổng hợp</code>. Phần mềm tự động đối chiếu số mẻ nấu (Khóa chính):
                        <ul>
                            <li>Nếu số mẻ <b>đã tồn tại</b> trên file Master: Ghi đè/cập nhật số liệu mới vào các ô thuộc dòng đó.</li>
                            <li>Nếu số mẻ <b>chưa tồn tại</b>: Tự động chèn thêm dòng mới vào cuối bảng.</li>
                            <li><b>Tự động Sắp xếp:</b> Sau khi gộp, toàn bộ bảng Master sẽ tự động được sắp xếp tăng dần theo Số mẻ nấu để bảng dữ liệu luôn khoa học.</li>
                        </ul>
                    </li>
                    <li>Sau khi hoàn tất, hệ thống sẽ báo cáo số lượng mẻ nấu đã cập nhật và chèn mới thành công kèm liên kết dẫn đến file sao lưu dự phòng.</li>
                </ol>
            </div>

            <hr style='border: none; border-top: 1px solid {border_color}; margin: 20px 0;'>

            <h2 style='color: #2A82DA; font-size: 16px;'>📋 CÚ PHÁP CÔNG THỨC & CÁC HÀM ĐƯỢC HỖ TRỢ</h2>
            <p>Hệ thống tự xây dựng bộ phân dịch công thức để tính toán trực tiếp giá trị trong bộ nhớ RAM mà không cần mở Excel. Bạn có thể sử dụng các phép toán số học, phép so sánh logic và các hàm lồng nhau.</p>
            
            <div style='background-color: {box_warning_bg}; border-left: 4px solid {box_warning_border}; padding: 10px; border-radius: 4px; margin-bottom: 15px;'>
                ⚠️ <b>QUY TẮC VIẾT CÔNG THỨC:</b>
                <ul style='margin: 6px 0 0 0; padding-left: 20px;'>
                    <li>Không phân biệt chữ hoa hay chữ thường (Ví dụ: <code>if</code>, <code>If</code> hay <code>IF</code> đều hợp lệ).</li>
                    <li>Tự động bỏ qua mọi khoảng trắng (Ví dụ: <code>A1 + B1</code> tương đương với <code>A1+B1</code>).</li>
                    <li>Hỗ trợ toán tử phần trăm <code>%</code> (Ví dụ: <code>E83%</code> tương đương với <code>E83 / 100</code>).</li>
                    <li>Hệ thống <b>không hỗ trợ</b> các hàm liên kết ngoài như VLOOKUP, INDEX, MATCH. Các hàm ngoài bảng tra cứu dưới đây nếu nhập vào sẽ gây lỗi <code>#NAME?</code>.</li>
                </ul>
            </div>

            <table style='width: 100%; border-collapse: collapse; margin-top: 10px;'>
                <thead>
                    <tr style='background-color: {main_header_bg}; color: {main_header_color};'>
                        <th style='border: 1px solid {border_color}; padding: 8px; width: 120px;'>Nhóm</th>
                        <th style='border: 1px solid {border_color}; padding: 8px; width: 140px;'>Hàm / Phép toán</th>
                        <th style='border: 1px solid {border_color}; padding: 8px;'>Diễn giải & Cú pháp</th>
                        <th style='border: 1px solid {border_color}; padding: 8px; width: 220px;'>Ví dụ thực tế ngành bia</th>
                    </tr>
                </thead>
                <tbody>
                    <!-- SỐ HỌC -->
                    <tr>
                        <td rowspan='3' style='border: 1px solid {border_color}; padding: 8px; font-weight: bold; vertical-align: middle; background-color: {th_bg_color};'>Số học</td>
                        <td style='border: 1px solid {border_color}; padding: 8px;'><code>+</code>, <code>-</code>, <code>*</code>, <code>/</code>, <code>^</code></td>
                        <td style='border: 1px solid {border_color}; padding: 8px;'>Cộng, trừ, nhân, chia, lũy thừa.</td>
                        <td style='border: 1px solid {border_color}; padding: 8px;'><code>(E83 / E78) * 100</code> (Tính hiệu suất thu hồi dịch đường)</td>
                    </tr>
                    <tr>
                        <td style='border: 1px solid {border_color}; padding: 8px;'><code>%</code></td>
                        <td style='border: 1px solid {border_color}; padding: 8px;'>Toán tử chia cho 100 (Hậu tố).</td>
                        <td style='border: 1px solid {border_color}; padding: 8px;'><code>E83 * 8%</code> (Tính hao hụt 8% thể tích mẻ nấu)</td>
                    </tr>
                    <tr>
                        <td style='border: 1px solid {border_color}; padding: 8px;'><code>&</code></td>
                        <td style='border: 1px solid {border_color}; padding: 8px;'>Nối các chuỗi văn bản lại với nhau.</td>
                        <td style='border: 1px solid {border_color}; padding: 8px;'><code>"Mẻ-" & H3</code> (Nối chữ "Mẻ-" với mã số ô H3)</td>
                    </tr>
                    <!-- LOGIC -->
                    <tr>
                        <td rowspan='3' style='border: 1px solid {border_color}; padding: 8px; font-weight: bold; vertical-align: middle; background-color: {th_bg_color};'>Logic & So sánh</td>
                        <td style='border: 1px solid {border_color}; padding: 8px;'><code>=</code>, <code>&lt;&gt;</code>, <code>&gt;</code>, <code>&lt;</code>, <code>&gt;=</code>, <code>&lt;=</code></td>
                        <td style='border: 1px solid {border_color}; padding: 8px;'>Bằng, khác, lớn hơn, nhỏ hơn, lớn hơn hoặc bằng, nhỏ hơn hoặc bằng.</td>
                        <td style='border: 1px solid {border_color}; padding: 8px;'><code>IF(E83 >= 140, "Đạt", "Thiếu")</code></td>
                    </tr>
                    <tr>
                        <td style='border: 1px solid {border_color}; padding: 8px;'><code>IF</code></td>
                        <td style='border: 1px solid {border_color}; padding: 8px;'><code>IF(điều_kiện, đúng, sai)</code><br>Hàm điều kiện rẽ nhánh (hỗ trợ lồng nhau).</td>
                        <td style='border: 1px solid {border_color}; padding: 8px;'><code>IF(F19>=F13, (F19-F13)*1440, 0)</code> (Tính thời gian trễ theo phút)</td>
                    </tr>
                    <tr>
                        <td style='border: 1px solid {border_color}; padding: 8px;'><code>AND</code>, <code>OR</code>, <code>NOT</code></td>
                        <td style='border: 1px solid {border_color}; padding: 8px;'>Các phép toán logic Và, Hoặc, Phủ định điều kiện.</td>
                        <td style='border: 1px solid {border_color}; padding: 8px;'><code>IF(AND(A1>0, B1="ĐẠT"), 1, 0)</code></td>
                    </tr>
                    <!-- THỐNG KÊ -->
                    <tr>
                        <td rowspan='3' style='border: 1px solid {border_color}; padding: 8px; font-weight: bold; vertical-align: middle; background-color: {th_bg_color};'>Toán & Thống kê</td>
                        <td style='border: 1px solid {border_color}; padding: 8px;'><code>SUM</code>, <code>AVERAGE</code></td>
                        <td style='border: 1px solid {border_color}; padding: 8px;'>Tính tổng hoặc trung bình cộng của dải ô hoặc các ô rời rạc.</td>
                        <td style='border: 1px solid {border_color}; padding: 8px;'><code>SUM(I78:I80)</code>, <code>AVERAGE(B10, B12, B14)</code></td>
                    </tr>
                    <tr>
                        <td style='border: 1px solid {border_color}; padding: 8px;'><code>MIN</code>, <code>MAX</code>, <code>COUNT</code></td>
                        <td style='border: 1px solid {border_color}; padding: 8px;'>Tìm giá trị nhỏ nhất, lớn nhất hoặc đếm số ô chứa số trong dải.</td>
                        <td style='border: 1px solid {border_color}; padding: 8px;'><code>MAX(D10:D40)</code> (Tìm nhiệt độ sôi lớn nhất)</td>
                    </tr>
                    <tr>
                        <td style='border: 1px solid {border_color}; padding: 8px;'><code>ROUND</code>, <code>ABS</code>, <code>MOD</code>, <code>INT</code></td>
                        <td style='border: 1px solid {border_color}; padding: 8px;'>Làm tròn số thập phân, trị tuyệt đối, chia lấy dư, lấy phần nguyên.</td>
                        <td style='border: 1px solid {border_color}; padding: 8px;'><code>ROUND(E83 / E78, 2)</code> (Làm tròn kết quả 2 số lẻ)</td>
                    </tr>
                    <!-- CHUỖI -->
                    <tr>
                        <td rowspan='2' style='border: 1px solid {border_color}; padding: 8px; font-weight: bold; vertical-align: middle; background-color: {th_bg_color};'>Xử lý Chuỗi</td>
                        <td style='border: 1px solid {border_color}; padding: 8px;'><code>LEFT</code>, <code>RIGHT</code>, <code>MID</code>, <code>LEN</code></td>
                        <td style='border: 1px solid {border_color}; padding: 8px;'>Cắt chuỗi từ bên trái, bên phải, ở giữa hoặc lấy độ dài của chuỗi.</td>
                        <td style='border: 1px solid {border_color}; padding: 8px;'><code>LEFT(H3, 4)</code> (Trích xuất 4 ký tự năm từ chuỗi mã số mẻ)</td>
                    </tr>
                    <tr>
                        <td style='border: 1px solid {border_color}; padding: 8px;'><code>TRIM</code>, <code>UPPER</code>, <code>LOWER</code></td>
                        <td style='border: 1px solid {border_color}; padding: 8px;'>Cắt bỏ khoảng trắng thừa, đổi thành chữ HOA, chữ thường.</td>
                        <td style='border: 1px solid {border_color}; padding: 8px;'><code>TRIM(UPPER(C5))</code> (Chuẩn hóa tên nguyên liệu đầu vào)</td>
                    </tr>
                    <!-- THỜI GIAN -->
                    <tr>
                        <td style='border: 1px solid {border_color}; padding: 8px; font-weight: bold; vertical-align: middle;'>Thời gian</td>
                        <td style='border: 1px solid {border_color}; padding: 8px;'><code>HOUR</code>, <code>MINUTE</code>, <code>SECOND</code></td>
                        <td style='border: 1px solid {border_color}; padding: 8px;'>Lấy giờ, phút, giây từ ô chứa ngày giờ hoặc từ số ngày Excel.</td>
                        <td style='border: 1px solid {border_color}; padding: 8px;'><code>HOUR(F13)</code> -> <code>23</code> (nếu F13 là 23:30)</td>
                    </tr>
                </tbody>
            </table>
        </div>
        """
        browser.setHtml(html_content)
        layout.addWidget(browser)

        btn = QPushButton("Đã Hiểu và Đóng", self)
        btn.setProperty("primary", True)
        btn.setStyleSheet("font-weight: bold;")
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)
