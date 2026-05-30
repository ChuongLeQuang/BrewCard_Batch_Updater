"""
EN: Dialog to manually select columns if auto-detect fails.
VI: Hộp thoại chọn cột thủ công nếu tự động nhận diện thất bại.
"""

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QLabel,
    QComboBox,
    QSpinBox,
    QDialogButtonBox,
    QHeaderView,
)
from PyQt6.QtCore import Qt
from openpyxl.utils import get_column_letter
from typing import List, Tuple


class ColumnSelectorDialog(QDialog):
    """
    EN: Lets user select Name/Formula columns from a data preview.
    VI: Cho phép người dùng chọn cột Tên/Công thức từ bảng xem trước.
    """

    def __init__(self, preview_data: List[List[str]], parent=None):
        super().__init__(parent)
        self.setWindowTitle("Xác định Thủ công Cột Dữ liệu")
        self.resize(800, 500)
        self.preview_data = preview_data
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        lbl_info = QLabel(
            "⚠️ <b>Hệ thống không tìm thấy tiêu đề tự động!</b><br>"
            "Vui lòng xem 20 dòng đầu tiên của file dưới đây và tự chỉ định cột tương ứng."
        )
        layout.addWidget(lbl_info)

        # Bảng xem trước
        max_cols = (
            max(len(row) for row in self.preview_data) if self.preview_data else 0
        )
        self.table = QTableWidget(len(self.preview_data), max_cols, self)

        letters = [get_column_letter(i + 1) for i in range(max_cols)]
        self.table.setHorizontalHeaderLabels(letters)
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Interactive
        )

        for r, row_data in enumerate(self.preview_data):
            for c, val in enumerate(row_data):
                item = QTableWidgetItem(str(val))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(r, c, item)

        layout.addWidget(self.table)

        # Khu vực chọn
        h_select = QHBoxLayout()

        h_select.addWidget(QLabel("Dòng bắt đầu đọc dữ liệu (vd: 5):"))
        self.spn_start_row = QSpinBox(self)
        self.spn_start_row.setMinimum(1)
        self.spn_start_row.setMaximum(9999)
        self.spn_start_row.setValue(2)
        h_select.addWidget(self.spn_start_row)

        h_select.addWidget(QLabel(" |  Cột chứa Tên:"))
        self.cmb_name = QComboBox(self)
        self.cmb_name.addItems(letters)
        h_select.addWidget(self.cmb_name)

        h_select.addWidget(QLabel(" |  Cột chứa Công thức:"))
        self.cmb_form = QComboBox(self)
        self.cmb_form.addItems(letters)
        h_select.addWidget(self.cmb_form)

        layout.addLayout(h_select)

        btn_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        btn_box.button(QDialogButtonBox.StandardButton.Ok).setText("Xác nhận & Nạp")
        btn_box.button(QDialogButtonBox.StandardButton.Cancel).setText("Hủy")
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)

    def get_selection(self) -> Tuple[int, int, int]:
        """EN: Returns (name_col_idx, form_col_idx, start_row). VI: Trả về (chỉ số cột Tên, chỉ số cột Form, dòng bắt đầu)."""
        return (
            self.cmb_name.currentIndex(),
            self.cmb_form.currentIndex(),
            self.spn_start_row.value(),
        )
