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
        self.resize(700, 550)
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
            border_color = "#555"
            th_bg_color = "#404040"
            code_bg_color = "#505050"
            code_text_color = "#AEEEEE"  # Light Cyan
            main_header_bg = "#333"
            main_header_color = "white"
        else:
            border_color = "#ccc"
            th_bg_color = "#f2f2f2"
            code_bg_color = "#e8e8e8"
            code_text_color = "black"
            main_header_bg = "#555"
            main_header_color = "white"

        html_content = f"""
        <h2 style='color: #2A82DA;'>1. HƯỚNG DẪN TỪNG PHÂN HỆ (TABS)</h2>
        <ul>
            <li style='margin-bottom: 8px;'><b>⚙️ Tab Cấu hình Hệ thống:</b> Chỉ làm 1 lần (hoặc khi có biểu mẫu mới). Tại đây bạn thiết lập các thông số:
                <ul style='margin-top: 4px;'>
                    <li><b>File tổng (Master):</b> Nơi dữ liệu sẽ được gom vào.</li>
                    <li><b>Tên Sheet lấy dữ liệu:</b> Nếu để trống, phần mềm sẽ quét <b>tất cả</b> các sheet có trong file con. Tiện lợi nhưng dễ quét nhầm vào các sheet rác.</li>
                    <li><b>Dấu hiệu nhận diện (Vân tay):</b> ⚠️ <b>CỰC KỲ QUAN TRỌNG!</b> Đây là "màng lọc" tự động để phân biệt sheet chứa dữ liệu thật và sheet rác. Bạn chọn một ô luôn có nội dung cố định để làm mốc (VD: <code>G3=Batch:</code>). Phần mềm sẽ kiểm tra ô G3, nếu chứa chữ "Batch:", nó mới lấy số liệu; nếu không, nó bỏ qua sheet đó để bảo vệ an toàn dữ liệu.<br>
                    <i>*Lưu ý: Nếu khai báo sai vân tay, phần mềm sẽ bỏ qua luôn cả sheet đúng. Có thể ghép nhiều điều kiện bằng dấu <code>&</code> (VD: <code>D3=Order: & G3=Batch:</code>).</i><br>
                    <i><b>*Mẹo sử dụng Form dự phòng:</b> Nếu công ty bạn dùng 2 biểu mẫu khác nhau (Form Mới và Form Cũ), hãy tạo 2 Profile với 2 Vân tay khác nhau. Ở Form chính, chọn "Form dự phòng" trỏ về Form phụ. Phần mềm sẽ tự động thử chìa khóa vân tay của cả 2 Form để nhận diện, nếu không khớp cả 2 thì nó mới kết luận đó là Sheet rác.</i></li>
                    <li><b>Bản đồ dữ liệu (Mappings):</b> Ghép nối cột đích với tọa độ ô tương ứng của file con.</li>
                </ul>
            </li>
            <li style='margin-bottom: 8px;'><b>📥 Tab Kiểm tra Chất lượng (QC):</b> Nơi làm việc hằng ngày. Kéo thả hàng chục file Excel vào đây. Phần mềm sẽ dựa vào Vân tay để nhận diện, tự quét lỗi tính toán, cảnh báo file hỏng.</li>
            <li><b>🚀 Tab Tổng hợp Dữ liệu:</b> Chạy gộp. Phần mềm tự đối chiếu Số lô (Batch), nếu trùng sẽ ghi đè (cập nhật), nếu mới sẽ chèn thêm dòng vào cuối.</li>
        </ul>
        <hr>
        <h2 style='color: #2A82DA;'>2. BẢNG TRA CỨU CÔNG THỨC & TỌA ĐỘ</h2>
        <p>Phần mềm hỗ trợ các công thức với cú pháp tương tự như Microsoft Excel. Bạn có thể kết hợp các hàm và phép toán dưới đây để tạo ra các công thức tính toán phức tạp.</p>
        <p>⚠️ <b>LƯU Ý:</b> Hệ thống <b>CHỈ HỖ TRỢ</b> các hàm được liệt kê trong bảng. Các hàm khác (VD: VLOOKUP) sẽ không hoạt động.</p>
        <style>
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ border: 1px solid {border_color}; padding: 6px; text-align: left; vertical-align: top; }}
            th {{ background-color: {th_bg_color}; }}
            code {{ background-color: {code_bg_color}; color: {code_text_color}; padding: 2px 4px; border-radius: 3px; }}
        </style>
        <table border='1' cellspacing='0' cellpadding='5'>
            <tr style='background-color: {main_header_bg}; color: {main_header_color};'><th>Nhóm</th><th>Hàm / Phép toán</th><th>Diễn giải & Cú pháp</th><th>Ví dụ</th></tr>
            
            <tr><td rowspan="6" style="vertical-align: middle;"><b>Cơ bản</b></td>
                <td><code>+</code>, <code>-</code>, <code>*</code>, <code>/</code></td><td>Các phép toán số học cơ bản.</td><td><code>(A1 + B1) * 2</code></td></tr>
            <tr><td><code>^</code></td><td>Phép lũy thừa.</td><td><code>A1 ^ 2</code></td></tr>
            <tr><td><code>&</code></td><td>Nối 2 chuỗi ký tự.</td><td><code>"ID-" & A1</code></td></tr>
            <tr><td><code>=</code>, <code>></code>, <code><</code></td><td>Các phép so sánh.</td><td><code>IF(A1 > 100, ...)</code></td></tr>
            <tr><td><code>>=</code>, <code><=</code>, <code><></code></td><td>Lớn hơn hoặc bằng, nhỏ hơn hoặc bằng, khác.</td><td><code>IF(A1 <> 0, ...)</code></td></tr>

            <tr><td rowspan="4" style="vertical-align: middle;"><b>Logic</b></td>
                <td><code>IF</code></td><td><code>IF(điều_kiện, giá_trị_đúng, giá_trị_sai)</code><br>Kiểm tra điều kiện.</td><td><code>IF(A1>100, "Tốt", "Kém")</code></td></tr>
            <tr><td><code>AND</code></td><td><code>AND(điều_kiện_1, điều_kiện_2, ...)</code><br>Đúng nếu TẤT CẢ đúng.</td><td><code>IF(AND(A1>0, B1<10), 1, 0)</code></td></tr>
            <tr><td><code>OR</code></td><td><code>OR(điều_kiện_1, điều_kiện_2, ...)</code><br>Đúng nếu CÓ BẤT KỲ điều kiện nào đúng.</td><td><code>IF(OR(A1="X", A1="Y"), 1, 0)</code></td></tr>
            <tr><td><code>NOT</code></td><td><code>NOT(điều_kiện)</code><br>Đảo ngược điều kiện.</td><td><code>IF(NOT(A1=0), "Khác 0", "")</code></td></tr>

            <tr><td rowspan="5" style="vertical-align: middle;"><b>Thống kê</b></td>
                <td><code>SUM</code></td><td><code>SUM(vùng_1, ô_2, ...)</code><br>Tính tổng.</td><td><code>SUM(A1:A10, C5)</code></td></tr>
            <tr><td><code>AVERAGE</code></td><td><code>AVERAGE(vùng_1, ...)</code><br>Tính trung bình cộng.</td><td><code>AVERAGE(B1:B10)</code></td></tr>
            <tr><td><code>COUNT</code></td><td><code>COUNT(vùng_1, ...)</code><br>Đếm các ô chứa SỐ.</td><td><code>COUNT(C1:C100)</code></td></tr>
            <tr><td><code>MAX</code></td><td><code>MAX(vùng_1, ...)</code><br>Tìm giá trị lớn nhất.</td><td><code>MAX(D1:D50)</code></td></tr>
            <tr><td><code>MIN</code></td><td><code>MIN(vùng_1, ...)</code><br>Tìm giá trị nhỏ nhất.</td><td><code>MIN(E1:E50)</code></td></tr>

            <tr><td rowspan="8" style="vertical-align: middle;"><b>Xử lý Chuỗi</b></td>
                <td><code>CONCATENATE</code></td><td><code>CONCATENATE(chuỗi_1, ...)</code><br>Nối chuỗi (giống dấu <code>&</code>).</td><td><code>CONCATENATE(A1, " ", B1)</code></td></tr>
            <tr><td><code>LEFT</code></td><td><code>LEFT(chuỗi, số_ký_tự)</code><br>Lấy ký tự bên trái.</td><td><code>LEFT(C2, 3)</code></td></tr>
            <tr><td><code>RIGHT</code></td><td><code>RIGHT(chuỗi, số_ký_tự)</code><br>Lấy ký tự bên phải.</td><td><code>RIGHT(D3, 5)</code></td></tr>
            <tr><td><code>MID</code></td><td><code>MID(chuỗi, vị_trí_bắt_đầu, số_ký_tự)</code><br>Lấy chuỗi ở giữa.</td><td><code>MID(E4, 2, 4)</code></td></tr>
            <tr><td><code>LEN</code></td><td><code>LEN(chuỗi)</code><br>Độ dài chuỗi.</td><td><code>LEN(F5)</code></td></tr>
            <tr><td><code>TRIM</code></td><td><code>TRIM(chuỗi)</code><br>Xóa khoảng trắng thừa.</td><td><code>TRIM(G6)</code></td></tr>
            <tr><td><code>UPPER</code></td><td><code>UPPER(chuỗi)</code><br>Chuyển thành chữ HOA.</td><td><code>UPPER(H7)</code></td></tr>
            <tr><td><code>LOWER</code></td><td><code>LOWER(chuỗi)</code><br>Chuyển thành chữ thường.</td><td><code>LOWER(I8)</code></td></tr>
        </table>
        """
        browser.setHtml(html_content)
        layout.addWidget(browser)

        btn = QPushButton("Đã Hiểu và Đóng", self)
        btn.setStyleSheet("font-weight: bold; padding: 8px;")
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)
