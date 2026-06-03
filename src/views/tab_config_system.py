"""
EN: Configuration System Tab.
VI: Phân hệ Cấu hình Hệ thống.
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QMessageBox,
    QFrame,
    QLabel,
)
from src.models.config_model import AppConfig
from src.views.dialog_guide import GuideDialog
from src.views.config_widget_profile import ConfigWidgetProfile
from src.views.config_widget_mappings import ConfigWidgetMappings
from src.utils.validation_utils import validate_fallback_fingerprint


class TabConfigSystem(QWidget):
    """
    EN: Widget for the System Configuration Tab.
    VI: Lớp giao diện cho Thẻ Cấu hình Hệ thống.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.config = AppConfig()
        self._setup_ui()
        self._setup_connections()
        self._load_data_to_ui()

    def _setup_ui(self) -> None:
        """EN: Initialize the UI layout. VI: Khởi tạo bố cục giao diện."""
        layout = QVBoxLayout(self)

        # Khung Hướng dẫn sử dụng (Help Box)
        frm_help = QFrame(self)
        frm_help.setStyleSheet(
            "QFrame { background-color: rgba(42, 130, 218, 0.1); border: 1px solid #2A82DA; border-radius: 5px; }"
        )
        h_help = QHBoxLayout(frm_help)
        lbl_help = QLabel(
            "💡 <b>HƯỚNG DẪN CẤU HÌNH (Chỉ thiết lập 1 lần):</b><br>"
            "Khai báo Tệp Đích để tổng hợp dữ liệu, thiết lập Tệp Đầu vào và xây dựng Bản đồ ánh xạ dữ liệu (Mappings).",
            self,
        )
        lbl_help.setStyleSheet("border: none; background: transparent;")
        h_help.addWidget(lbl_help, stretch=1)

        btn_show_guide = QPushButton("📖 Xem chi tiết Hướng dẫn & Công thức", self)
        btn_show_guide.clicked.connect(lambda: GuideDialog(self).exec())
        h_help.addWidget(btn_show_guide)
        layout.addWidget(frm_help)

        # Khối Giao diện cấu hình Profile
        self.widget_profile = ConfigWidgetProfile(self)
        layout.addWidget(self.widget_profile)

        # Khối Giao diện Bản đồ Mappings
        self.widget_mappings = ConfigWidgetMappings(self)
        layout.addWidget(self.widget_mappings)

        # Nút Lưu Cấu Hình
        btn_save = QPushButton("💾 Lưu Cấu Hình (Lưu đè / Tạo mới)", self)
        btn_save.clicked.connect(self._save_config)
        btn_save.setStyleSheet(
            "background-color: #28A745; color: white; font-weight: bold; padding: 8px;"
        )
        layout.addWidget(btn_save)

    def _setup_connections(self) -> None:
        """EN: Setup signal connections. VI: Cài đặt các tín hiệu nối 2 Widget."""
        self.widget_profile.headers_refreshed.connect(
            self.widget_mappings.update_headers
        )
        self.widget_profile.profile_changed.connect(self._load_profile)
        self.widget_profile.delete_requested.connect(self._delete_profile)

    def _load_profile(self, profile_name: str) -> None:
        """EN: Load selected profile. VI: Tải cấu hình được chọn."""
        if profile_name and profile_name != self.config.profile_name:
            self.config = AppConfig(profile_name)
            self._load_data_to_ui()

    def _delete_profile(self, profile_name: str) -> None:
        """EN: Delete profile. VI: Xóa cấu hình."""
        if profile_name == "BrewCard":
            QMessageBox.warning(
                self, "Cảnh báo", "Không thể xóa cấu hình gốc (BrewCard)!"
            )
            return

        reply = QMessageBox.question(
            self,
            "Xóa cấu hình",
            f"Bạn có chắc muốn xóa cấu hình '{profile_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.config.delete_profile()
            self.config = AppConfig("BrewCard")
            self._load_data_to_ui()

    def _load_data_to_ui(self) -> None:
        """EN: Load data to UI. VI: Tải dữ liệu lên giao diện."""
        all_profiles = AppConfig.get_all_profiles()
        self.widget_profile.load_data(
            self.config.data, self.config.profile_name, all_profiles
        )
        self.widget_mappings.load_mappings(self.config.data.get("mappings", []))

    def _save_config(self) -> None:
        """EN: Save UI data to JSON. VI: Lưu dữ liệu từ UI xuống JSON."""
        try:
            profile_data = self.widget_profile.get_data()
        except ValueError as e:
            QMessageBox.warning(self, "Lỗi Nhập liệu", str(e))
            return

        if not profile_data["profile_name"]:
            QMessageBox.warning(
                self, "Lỗi", "Vui lòng nhập Tên Hồ sơ cấu hình (Profile)!"
            )
            return

        temp_config = AppConfig(profile_data["profile_name"])
        temp_config.data.update(profile_data)
        fp_valid, fallback_name = validate_fallback_fingerprint(temp_config)
        if not fp_valid:
            QMessageBox.warning(
                self,
                "Lỗi Form dự phòng",
                f"Hồ sơ dự phòng '{fallback_name}' hiện đang để trống Dấu vân tay!\n\n"
                "Để đảm bảo an toàn, Form dự phòng BẮT BUỘC phải có dấu vân tay. "
                f"Vui lòng chuyển sang Profile '{fallback_name}' và thiết lập vân tay cho nó trước.",
            )
            return

        self.config.profile_name = profile_data["profile_name"]
        self.config.data.update(profile_data)
        self.config.data["mappings"] = self.widget_mappings.get_mappings()

        self.config.save()

        self._load_data_to_ui()  # Reload UI
        QMessageBox.information(
            self, "Thành công", f"Đã lưu cấu hình: '{self.config.profile_name}'"
        )
