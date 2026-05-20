"""
EN: Main application window.
VI: Cửa sổ chính của ứng dụng.
"""

from PyQt6.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout
from PyQt6.QtGui import QAction
from src.config.constants import APP_NAME, APP_VERSION, WINDOW_WIDTH, WINDOW_HEIGHT
from src.utils.theme_manager import ThemeManager
from src.views.tab_config_system import TabConfigSystem
from src.views.tab_qc_check import TabQCCheck
from src.views.tab_sync_data import TabSyncData


class MainWindow(QMainWindow):
    """
    EN: The main application window containing the tab widget and menus.
    VI: Cửa sổ ứng dụng chính chứa các thẻ (tabs) và thanh thực đơn.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self._setup_ui()
        self._setup_menu()

    def _setup_ui(self) -> None:
        """EN: Setup central widget and tabs. VI: Thiết lập giao diện trung tâm và các thẻ."""
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.tab_widget = QTabWidget(central_widget)

        # Khởi tạo và gắn 3 phân hệ Tab chính
        self.tab_config = TabConfigSystem(self)
        self.tab_qc = TabQCCheck(self)
        self.tab_sync = TabSyncData(self)

        self.tab_widget.addTab(self.tab_config, "⚙️ Cấu hình Hệ thống")
        self.tab_widget.addTab(self.tab_qc, "📥 Kiểm tra Chất lượng (QC)")
        self.tab_widget.addTab(self.tab_sync, "🚀 Tổng hợp Dữ liệu")

        # Kết nối tín hiệu giữa các tab
        self.tab_qc.scan_completed.connect(self.tab_sync.on_qc_scan_completed)

        layout.addWidget(self.tab_widget)
        self.statusBar().showMessage("Phần mềm đã sẵn sàng.")

    def _setup_menu(self) -> None:
        """EN: Setup the menu bar for themes. VI: Thiết lập thanh thực đơn chuyển đổi giao diện."""
        menu_bar = self.menuBar()
        theme_menu = menu_bar.addMenu("Giao diện")

        modes = [
            ("Theo Hệ thống", "system"),
            ("Sáng (Light Mode)", "light"),
            ("Tối (Dark Mode)", "dark"),
        ]

        for title, mode in modes:
            action = QAction(title, self)
            action.triggered.connect(lambda checked, m=mode: self._change_theme(m))
            theme_menu.addAction(action)

    def _change_theme(self, mode: str) -> None:
        from PyQt6.QtWidgets import QApplication

        ThemeManager.apply_theme(QApplication.instance(), mode)
        self.statusBar().showMessage(
            f"Đã chuyển giao diện sang chế độ: {mode.capitalize()}"
        )
