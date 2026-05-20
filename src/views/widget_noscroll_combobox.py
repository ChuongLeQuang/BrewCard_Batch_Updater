"""
EN: Custom QComboBox that ignores mouse wheel scrolling.
VI: Lớp QComboBox tùy chỉnh bỏ qua sự kiện cuộn chuột.
"""

from PyQt6.QtWidgets import QComboBox, QWidget
from PyQt6.QtGui import QWheelEvent


class NoScrollComboBox(QComboBox):
    """
    EN: Custom QComboBox that ignores mouse wheel scrolling.
    VI: Lớp QComboBox tùy chỉnh bỏ qua sự kiện cuộn chuột để tránh thay đổi dữ liệu ngoài ý muốn.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

    def wheelEvent(self, event: QWheelEvent) -> None:
        event.ignore()
