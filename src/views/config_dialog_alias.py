"""
EN: Dialog for manual human-in-the-loop mapping of unknown columns.
VI: Hộp thoại cảnh báo ghép nối thủ công cho các cột không rõ tên.
"""

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QLabel,
    QComboBox,
    QDialogButtonBox,
    QCompleter,
)
from PyQt6.QtCore import Qt
import difflib


class AliasMappingDialog(QDialog):
    """
    EN: Dialog for manually mapping unmatched columns during import.
    VI: Hộp thoại cho phép người dùng chọn Cột đích thủ công cho các tên cột không khớp.
    """

    def __init__(self, pending_aliases: list, target_info: dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ghép nối Công thức Thủ công")
        self.resize(800, 400)
        self.pending_aliases = pending_aliases
        self.target_info = target_info
        self.target_names = sorted(list(target_info.keys()))
        self.comboboxes = []
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        lbl = QLabel(
            "⚠️ <b>Phát hiện các cột có tên không khớp chuẩn!</b><br>"
            "Vui lòng chọn Cột đích tương ứng để nạp công thức, hoặc chọn 'Bỏ qua'.",
            self,
        )
        layout.addWidget(lbl)

        self.table = QTableWidget(len(self.pending_aliases), 3, self)
        self.table.setHorizontalHeaderLabels(
            ["Tên cột (Khách gửi)", "Công thức", "Ghép vào Cột chuẩn"]
        )

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        self.table.setColumnWidth(0, 200)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        self.table.setColumnWidth(1, 200)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)

        self.table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)

        for row, (raw_name, raw_form) in enumerate(self.pending_aliases):
            item_name = QTableWidgetItem(raw_name)
            self.table.setItem(row, 0, item_name)

            item_form = QTableWidgetItem(raw_form)
            item_form.setFlags(item_form.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row, 1, item_form)

            cmb = QComboBox(self)
            cmb.setEditable(True)
            cmb.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
            cmb.addItem("❌ Bỏ qua (Không nạp)", userData="❌")

            best_match = None
            best_score = 0.0

            for t_name, t_form in self.target_info.items():
                name_score = difflib.SequenceMatcher(
                    None, raw_name.lower(), t_name.lower()
                ).ratio()
                formula_score = 0.0
                if raw_form and t_form:
                    formula_score = difflib.SequenceMatcher(
                        None, raw_form.lower(), t_form.lower()
                    ).ratio()
                elif not raw_form and not t_form:
                    formula_score = 1.0

                total_score = (name_score * 0.6) + (formula_score * 0.4)
                if total_score > best_score:
                    best_score = total_score
                    best_match = t_name

            suggested_index = 0
            for i, t_name in enumerate(self.target_names):
                display_text = t_name
                if best_match and t_name == best_match and best_score >= 0.8:
                    display_text = f"⭐ {t_name} (Giống {int(best_score*100)}%)"
                    suggested_index = i + 1
                cmb.addItem(display_text, userData=t_name)

            if suggested_index > 0:
                cmb.setCurrentIndex(suggested_index)

            completer = cmb.completer()
            if completer:
                completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
                completer.setFilterMode(Qt.MatchFlag.MatchContains)
                completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

            self.table.setCellWidget(row, 2, cmb)
            self.comboboxes.append((row, raw_name, cmb))

        layout.addWidget(self.table)

        btn_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        btn_box.button(QDialogButtonBox.StandardButton.Ok).setText("Xác nhận & Nạp")
        btn_box.button(QDialogButtonBox.StandardButton.Cancel).setText("Hủy toàn bộ")
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)

    def get_results(self) -> dict:
        """EN: Return a dict of mapped aliases. VI: Trả về từ điển kết quả ghép nối."""
        results = {}
        for row, raw_name, cmb in self.comboboxes:
            idx = cmb.currentIndex()
            if idx >= 0:
                selected = cmb.itemData(idx)
            else:
                typed = cmb.currentText().strip()
                selected = next(
                    (t for t in self.target_names if t.lower() == typed.lower()), None
                )

            if selected and selected != "❌":
                item = self.table.item(row, 0)
                final_name = item.text().strip() if item else raw_name
                results[raw_name] = (final_name, selected)
        return results
