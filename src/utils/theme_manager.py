"""
EN: Theme manager for PyQt6 application.
VI: Quản lý giao diện (Theme) cho ứng dụng PyQt6.
"""

import darkdetect
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt


class ThemeManager:
    """
    EN: Handles switching between Light, Dark, and System themes.
    VI: Xử lý chuyển đổi giữa các giao diện Sáng, Tối và Hệ thống.
    """

    @staticmethod
    def apply_theme(app: QApplication, mode: str = "system") -> None:
        """
        EN: Apply the selected theme to the application.
        VI: Áp dụng giao diện được chọn cho ứng dụng.
        """
        if mode == "system":
            mode = "dark" if darkdetect.isDark() else "light"

        app.setStyle("Fusion")

        if mode == "dark":
            ThemeManager._apply_dark_theme(app)
        else:
            ThemeManager._apply_light_theme(app)

    @staticmethod
    def _apply_dark_theme(app: QApplication) -> None:
        """EN: Apply dark palette. VI: Áp dụng bảng màu tối."""
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
        app.setPalette(palette)

    @staticmethod
    def _apply_light_theme(app: QApplication) -> None:
        """EN: Reset to default light palette. VI: Khôi phục bảng màu sáng mặc định."""
        app.setPalette(app.style().standardPalette())
