"""
EN: Main entry point of the BrewCard_Batch_Updater project.
VI: Điểm bắt đầu (Entry point) của dự án BrewCard_Batch_Updater.
"""

import sys
import os
import logging
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from src.views.main_window import MainWindow
from src.utils.theme_manager import ThemeManager
from src.utils.core_utils import get_project_root


def main():
    # Khắc phục lỗi Windows gom nhóm và làm mờ icon trên Taskbar
    import platform

    if platform.system() == "Windows":
        import ctypes

        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                "brewcard.batch.updater.1.0"
            )
        except Exception as e:
            logging.debug(f"Could not set AppUserModelID: {e}")

    app = QApplication(sys.argv)

    # Load App Icon
    icon_path = os.path.join(get_project_root(), "assets", "icon.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    ThemeManager.apply_theme(app, "system")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
