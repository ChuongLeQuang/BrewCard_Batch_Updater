"""
EN: Custom exceptions for the application.
VI: Các lớp ngoại lệ tự định nghĩa cho ứng dụng.
"""


class ConfigNotFoundError(Exception):
    """EN: Raised when a configuration profile is not found. VI: Lỗi khi không tìm thấy hồ sơ cấu hình."""

    pass


class InvalidTemplateError(Exception):
    """EN: Raised when an input Excel file does not match the expected template. VI: Lỗi khi tệp Excel đầu vào không khớp với mẫu."""

    pass
