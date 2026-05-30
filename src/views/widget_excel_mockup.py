"""
EN: Excel mockup widget for picking cell coordinates.
VI: Giao diện mô phỏng Excel để chọn tọa độ ô.
"""

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QTableWidget,
    QPushButton,
    QHBoxLayout,
    QLabel,
    QHeaderView,
)
from PyQt6.QtCore import Qt


class WidgetExcelMockup(QDialog):
    """
    EN: Dialog showing a grid to pick an Excel cell coordinate (e.g., C3).
    VI: Hộp thoại hiển thị lưới để chọn tọa độ ô Excel (vd: C3).
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Chọn Tọa Độ Ô (Excel Mockup)")
        self.resize(600, 400)
        self.selected_cell: str = ""
        self._setup_ui()

    def _setup_ui(self) -> None:
        """EN: Initialize the UI layout. VI: Khởi tạo bố cục giao diện."""
        layout = QVBoxLayout(self)

        lbl = QLabel("Vui lòng click đúp vào ô hoặc chọn ô và bấm 'Xác nhận'", self)
        layout.addWidget(lbl)

        # Tạo bảng 50 dòng, 26 cột (A-Z)
        self.table = QTableWidget(50, 26, self)
        letters = [chr(65 + i) for i in range(26)]
        self.table.setHorizontalHeaderLabels(letters)
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        btn_ok = QPushButton("Xác nhận", self)
        btn_cancel = QPushButton("Hủy", self)

        btn_ok.clicked.connect(self._on_accept)
        btn_cancel.clicked.connect(self.reject)
        self.table.cellDoubleClicked.connect(lambda r, c: self._on_accept())

        btn_layout.addStretch()
        btn_layout.addWidget(btn_ok)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

    def _on_accept(self) -> None:
        """EN: Handle accept button. VI: Xử lý sự kiện nút xác nhận hoặc click đúp."""
        curr = self.table.currentItem()
        if curr is not None:
            self.selected_cell = f"{chr(65 + curr.column())}{curr.row() + 1}"
        self.accept()
