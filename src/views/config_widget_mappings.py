"""
EN: Data Mappings Table Widget.
VI: Widget quản lý bảng lưới ánh xạ dữ liệu.
"""

import re
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QComboBox,
    QMessageBox,
    QDialog,
)
from PyQt6.QtCore import Qt
from src.views.widget_noscroll_combobox import NoScrollComboBox
from src.views.widget_excel_mockup import WidgetExcelMockup


class ConfigWidgetMappings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.letter_to_name = {}
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(QLabel("Bản đồ ánh xạ dữ liệu (Mappings):", self))
        self.tbl_mappings = QTableWidget(0, 3, self)
        self.tbl_mappings.setHorizontalHeaderLabels(
            [
                "Cột đích (Chữ cái)",
                "Tên Cột đích (Tự động)",
                "Nguồn lấy dữ liệu / Công thức Excel",
            ]
        )

        header = self.tbl_mappings.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        self.tbl_mappings.setColumnWidth(0, 150)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tbl_mappings)

        h_btns = QHBoxLayout()
        btn_add = QPushButton("➕ Thêm dòng ánh xạ", self)
        btn_add.clicked.connect(lambda: self._add_mapping_row("", "", "", True))
        btn_pick = QPushButton("🎯 Mở Excel ảo chọn Ô", self)
        btn_pick.clicked.connect(self._open_excel_mockup)
        h_btns.addWidget(btn_add)
        h_btns.addWidget(btn_pick)
        layout.addLayout(h_btns)

        self.tbl_mappings.cellChanged.connect(self._on_cell_changed)

    def _on_cell_changed(self, row: int, col: int):
        item = self.tbl_mappings.item(row, col)
        if not item or not item.text().strip():
            return

        self.tbl_mappings.blockSignals(True)
        if col == 2:
            formatted = re.sub(
                r"\s*([()*/+<>=^&,\-])\s*", r"\1", item.text().strip().upper()
            )
            item.setText(formatted)
        self.tbl_mappings.blockSignals(False)

    def update_headers(self, letter_to_name: dict):
        self.letter_to_name = letter_to_name
        for row in range(self.tbl_mappings.rowCount()):
            cmb = self.tbl_mappings.cellWidget(row, 0)
            if isinstance(cmb, QComboBox):
                current_val = cmb.currentText().upper()
                cmb.blockSignals(True)
                cmb.clear()
                sorted_letters = sorted(
                    list(self.letter_to_name.keys()), key=lambda l: (len(l), l)
                )
                cmb.addItems(sorted_letters)
                if current_val and cmb.findText(current_val) == -1:
                    cmb.addItem(current_val)
                cmb.setCurrentText(current_val)
                cmb.blockSignals(False)
                self._update_target_name(row, cmb.currentText())

    def _update_target_name(self, row: int, col_letter: str):
        item = self.tbl_mappings.item(row, 1)
        if item:
            item.setText(self.letter_to_name.get(col_letter.strip().upper(), ""))

    def _add_mapping_row(
        self,
        target_col: str,
        target_letter: str,
        source_mapping: str,
        scroll_to_bottom: bool = False,
    ):
        row = self.tbl_mappings.rowCount()
        self.tbl_mappings.insertRow(row)

        cmb = NoScrollComboBox(self)
        cmb.setEditable(True)
        sorted_letters = sorted(
            list(self.letter_to_name.keys()), key=lambda l: (len(l), l)
        )
        cmb.addItems(sorted_letters)
        if target_letter and cmb.findText(target_letter.upper()) == -1:
            cmb.addItem(target_letter.upper())
        cmb.setCurrentText(target_letter.upper())
        self.tbl_mappings.setCellWidget(row, 0, cmb)

        item_name = QTableWidgetItem(target_col)
        item_name.setFlags(item_name.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.tbl_mappings.setItem(row, 1, item_name)
        self.tbl_mappings.setItem(row, 2, QTableWidgetItem(source_mapping))

        cmb.currentTextChanged.connect(
            lambda text, r=row: self._update_target_name(r, text)
        )
        if target_letter:
            self._update_target_name(row, target_letter)
        if scroll_to_bottom:
            self.tbl_mappings.scrollToBottom()

    def _open_excel_mockup(self):
        dialog = WidgetExcelMockup(self)
        if dialog.exec() == QDialog.DialogCode.Accepted and dialog.selected_cell:
            curr = self.tbl_mappings.currentItem()
            if curr and curr.column() == 2:
                curr.setText(dialog.selected_cell)
            else:
                QMessageBox.information(
                    self,
                    "Tọa độ",
                    f"Đã chọn ô {dialog.selected_cell}\n(Ghi chú: Hãy click chọn trước một ô ở cột 'Nguồn' để phần mềm điền tự động)",
                )

    def load_mappings(self, mappings: list):
        self.tbl_mappings.setUpdatesEnabled(False)
        self.tbl_mappings.setRowCount(0)
        for m in mappings:
            self._add_mapping_row(
                m.get("target_col", ""),
                m.get("target_col_letter", ""),
                m.get("source_mapping", ""),
            )
        self.tbl_mappings.setUpdatesEnabled(True)

    def get_mappings(self) -> list:
        mappings = []
        for row in range(self.tbl_mappings.rowCount()):
            cmb = self.tbl_mappings.cellWidget(row, 0)
            tcl = (
                cmb.currentText().strip().upper() if isinstance(cmb, QComboBox) else ""
            )
            tc_item = self.tbl_mappings.item(row, 1)
            src_item = self.tbl_mappings.item(row, 2)
            mappings.append(
                {
                    "target_col": tc_item.text().strip() if tc_item else "",
                    "target_col_letter": tcl,
                    "source_mapping": src_item.text().strip() if src_item else "",
                }
            )
        return mappings
