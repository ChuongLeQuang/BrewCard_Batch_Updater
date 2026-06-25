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
            app.setStyleSheet(ThemeManager._get_dark_qss())
        else:
            ThemeManager._apply_light_theme(app)
            app.setStyleSheet(ThemeManager._get_light_qss())

    @staticmethod
    def _apply_dark_theme(app: QApplication) -> None:
        """EN: Apply dark palette. VI: Áp dụng bảng màu tối."""
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(32, 32, 32))
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Base, QColor(43, 43, 43))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(32, 32, 32))
        palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Button, QColor(45, 45, 45))
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
        app.setPalette(palette)

    @staticmethod
    def _apply_light_theme(app: QApplication) -> None:
        """EN: Reset to default light palette. VI: Khôi phục bảng màu sáng mặc định."""
        app.setPalette(app.style().standardPalette())

    @staticmethod
    def _get_dark_qss() -> str:
        return """
        QWidget {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            font-size: 12px;
            color: #ffffff;
        }
        QMainWindow, QDialog {
            background-color: #202020;
        }
        
        /* Tab Widget Styling (Fluent pivot look) */
        QTabWidget::pane {
            border: 1px solid #3d3d3d;
            border-radius: 6px;
            background-color: #2b2b2b;
            top: -1px;
        }
        QTabWidget::tab-bar {
            left: 5px;
        }
        QTabBar::tab {
            background-color: transparent;
            color: #b0b0b0;
            padding: 8px 16px;
            margin-right: 4px;
            border-bottom: 2px solid transparent;
            font-weight: bold;
        }
        QTabBar::tab:hover {
            background-color: rgba(255, 255, 255, 0.05);
            color: #ffffff;
            border-radius: 4px;
        }
        QTabBar::tab:selected {
            background-color: #2b2b2b;
            color: #2A82DA;
            border-bottom: 3px solid #2A82DA;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }

        /* Buttons Styling (Fluent buttons) */
        QPushButton {
            background-color: #2d2d2d;
            border: 1px solid #444444;
            border-radius: 6px;
            padding: 6px 14px;
            min-height: 18px;
            color: #ffffff;
            font-weight: 500;
        }
        QPushButton:hover {
            background-color: #383838;
            border-color: #2A82DA;
        }
        QPushButton:pressed {
            background-color: #1e1e1e;
            border-color: #1c5d9b;
        }
        QPushButton:disabled {
            background-color: #1a1a1a;
            border-color: #2b2b2b;
            color: #666666;
        }
        /* Primary Button */
        QPushButton[primary="true"] {
            background-color: #0078d4;
            border-color: #0078d4;
            color: #ffffff;
            font-weight: bold;
        }
        QPushButton[primary="true"]:hover {
            background-color: #0067b8;
            border-color: #0067b8;
        }
        QPushButton[primary="true"]:pressed {
            background-color: #005a9e;
            border-color: #005a9e;
        }

        /* QTextBrowser Styling */
        QTextBrowser {
            background-color: #2d2d2d;
            border: 1px solid #3d3d3d;
            border-radius: 6px;
            padding: 10px;
        }

        /* Inputs (LineEdit, ComboBox) */
        QLineEdit, QComboBox {
            background-color: #2d2d2d;
            border: 1px solid #444444;
            border-radius: 5px;
            padding: 5px 8px;
            color: #ffffff;
            min-height: 16px;
        }
        QLineEdit:focus, QComboBox:focus {
            border: 1px solid #2A82DA;
            border-bottom: 2px solid #2A82DA;
        }
        
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 15px;
            border-left-width: 0px;
        }
        QComboBox QAbstractItemView {
            background-color: #2d2d2d;
            border: 1px solid #444444;
            selection-background-color: #2A82DA;
            selection-color: #ffffff;
        }

        /* Table Widget (Modern Flat Table) */
        QTableWidget {
            background-color: #2d2d2d;
            border: 1px solid #3d3d3d;
            gridline-color: #3d3d3d;
            border-radius: 6px;
            selection-background-color: rgba(42, 130, 218, 0.3);
            selection-color: #ffffff;
            alternate-background-color: #252525;
        }
        QHeaderView::section {
            background-color: #262626;
            color: #ffffff;
            padding: 6px;
            border: none;
            border-bottom: 1px solid #3d3d3d;
            border-right: 1px solid #3d3d3d;
            font-weight: bold;
        }
        QTableWidget QTableCornerButton::section {
            background-color: #262626;
            border: none;
        }
        
        /* ScrollBars */
        QScrollBar:vertical {
            border: none;
            background: #202020;
            width: 8px;
            margin: 0px;
        }
        QScrollBar::handle:vertical {
            background: #444444;
            min-height: 20px;
            border-radius: 4px;
        }
        QScrollBar::handle:vertical:hover {
            background: #666666;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
        """

    @staticmethod
    def _get_light_qss() -> str:
        return """
        QWidget {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            font-size: 12px;
            color: #2c3e50;
        }
        QMainWindow, QDialog {
            background-color: #f3f3f3;
        }
        
        /* Tab Widget Styling (Fluent pivot look) */
        QTabWidget::pane {
            border: 1px solid #dcdde1;
            border-radius: 6px;
            background-color: #ffffff;
            top: -1px;
        }
        QTabWidget::tab-bar {
            left: 5px;
        }
        QTabBar::tab {
            background-color: transparent;
            color: #718093;
            padding: 8px 16px;
            margin-right: 4px;
            border-bottom: 2px solid transparent;
            font-weight: bold;
        }
        QTabBar::tab:hover {
            background-color: rgba(0, 0, 0, 0.05);
            color: #2f3640;
            border-radius: 4px;
        }
        QTabBar::tab:selected {
            background-color: #ffffff;
            color: #2A82DA;
            border-bottom: 3px solid #2A82DA;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }

        /* Buttons Styling (Fluent buttons) */
        QPushButton {
            background-color: #ffffff;
            border: 1px solid #dcdde1;
            border-radius: 6px;
            padding: 6px 14px;
            min-height: 18px;
            color: #2f3640;
            font-weight: 500;
        }
        QPushButton:hover {
            background-color: #f5f6fa;
            border-color: #2A82DA;
        }
        QPushButton:pressed {
            background-color: #e5e5e5;
            border-color: #1c5d9b;
        }
        QPushButton:disabled {
            background-color: #f5f6fa;
            border-color: #e1b12c;
            color: #718093;
        }
        /* Primary Button */
        QPushButton[primary="true"] {
            background-color: #0078d4;
            border-color: #0078d4;
            color: #ffffff;
            font-weight: bold;
        }
        QPushButton[primary="true"]:hover {
            background-color: #0067b8;
            border-color: #0067b8;
        }
        QPushButton[primary="true"]:pressed {
            background-color: #005a9e;
            border-color: #005a9e;
        }

        /* QTextBrowser Styling */
        QTextBrowser {
            background-color: #ffffff;
            border: 1px solid #dcdde1;
            border-radius: 6px;
            padding: 10px;
        }

        /* Inputs (LineEdit, ComboBox) */
        QLineEdit, QComboBox {
            background-color: #ffffff;
            border: 1px solid #dcdde1;
            border-radius: 5px;
            padding: 5px 8px;
            color: #2f3640;
            min-height: 16px;
        }
        QLineEdit:focus, QComboBox:focus {
            border: 1px solid #2A82DA;
            border-bottom: 2px solid #2A82DA;
        }
        
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 15px;
            border-left-width: 0px;
        }
        QComboBox QAbstractItemView {
            background-color: #ffffff;
            border: 1px solid #dcdde1;
            selection-background-color: #2A82DA;
            selection-color: #ffffff;
        }

        /* Table Widget (Modern Flat Table) */
        QTableWidget {
            background-color: #ffffff;
            border: 1px solid #dcdde1;
            gridline-color: #dcdde1;
            border-radius: 6px;
            selection-background-color: rgba(42, 130, 218, 0.15);
            selection-color: #2f3640;
            alternate-background-color: #f8f9fa;
        }
        QHeaderView::section {
            background-color: #f5f6fa;
            color: #2f3640;
            padding: 6px;
            border: none;
            border-bottom: 1px solid #dcdde1;
            border-right: 1px solid #dcdde1;
            font-weight: bold;
        }
        QTableWidget QTableCornerButton::section {
            background-color: #f5f6fa;
            border: none;
        }
        
        /* ScrollBars */
        QScrollBar:vertical {
            border: none;
            background: #f3f3f3;
            width: 8px;
            margin: 0px;
        }
        QScrollBar::handle:vertical {
            background: #dcdde1;
            min-height: 20px;
            border-radius: 4px;
        }
        QScrollBar::handle:vertical:hover {
            background: #b2bec3;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
        """
