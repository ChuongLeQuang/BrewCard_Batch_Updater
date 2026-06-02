"""
EN: Central configuration for application constants.
VI: Cấu hình trung tâm lưu trữ các hằng số của ứng dụng.
"""

APP_NAME = "Trình Cập nhật Mẻ nấu BrewCard"
APP_VERSION = "1.0.0"

# Kích thước cửa sổ mặc định (Window Dimensions)
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700

# Màu sắc giao diện (UI Colors)
COLOR_ERROR_TEXT = "#FF3333"  # Đỏ cho trạng thái lỗi QC
COLOR_SUCCESS_TEXT = "#28A745"  # Xanh lá cho trạng thái thành công

# Từ khóa nhận diện cột khi nạp file công thức tự động (Smart Auto-Import)
IMPORT_NAME_KEYWORDS = ["tên", "cột", "name", "target", "đích", "trường"]
IMPORT_FORMULA_KEYWORDS = ["công thức", "formula", "source", "nguồn", "dữ liệu"]

# Định dạng hiển thị dữ liệu (Number Formatting)
# Ánh xạ tên thân thiện sang mã định dạng của OpenPyXL.
FORMAT_OPTIONS = {
    "📝 Mặc định": "General",
    "🔤 Văn bản": "@",
    "🔢 Số nguyên": "0",
    "🧮 Số thập phân (1)": "0.0",
    "🧮 Số thập phân (2)": "0.00",
    "🧮 Số thập phân (3)": "0.000",
    "📊 Phần trăm (0%)": "0%",
    "📊 Phần trăm (0.00%)": "0.00%",
    "📅 Ngày (dd/mm/yyyy)": "dd/mm/yyyy",
    "⏰ Ngày & Giờ (dd/mm/yyyy hh:mm)": "dd/mm/yyyy hh:mm",
}
