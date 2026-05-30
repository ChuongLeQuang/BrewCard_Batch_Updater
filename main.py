"""
EN: Main entry point of the BrewCard_Batch_Updater project.
VI: Điểm bắt đầu (Entry point) của dự án BrewCard_Batch_Updater.
"""

import sys
from PyQt6.QtWidgets import QApplication
from src.views.main_window import MainWindow
from src.utils.theme_manager import ThemeManager


def main():
    app = QApplication(sys.argv)

    ThemeManager.apply_theme(app, "system")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
