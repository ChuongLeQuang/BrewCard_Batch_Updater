"""
EN: Quality Control (QC) Check Tab.
VI: Phân hệ Kiểm tra Chất lượng (QC).
"""

import os
from typing import List, Dict, Any

from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QHeaderView,
    QDialog,
    QPushButton,
    QHBoxLayout,
    QProgressBar,
    QTableWidgetItem,
    QMessageBox,
    QAbstractItemView,
    QFrame,
    QListWidget,
    QListWidgetItem,
    QDialogButtonBox,
)

import openpyxl
from src.models.config_model import AppConfig
from src.models.excel_data_model import BrewRecord
from src.controllers.worker_threads import QCWorker
from src.utils.qc_logger import log_qc_errors
from src.config.constants import COLOR_ERROR_TEXT, COLOR_SUCCESS_TEXT


class FileScannerWorker(QThread):
    """Luồng ngầm quét danh sách sheet để không làm treo UI."""

    file_scanned = pyqtSignal(str, list, str)
    finished_scan = pyqtSignal()

    def __init__(self, file_paths: List[str], parent=None):
        super().__init__(parent)
        self.file_paths = file_paths

    def run(self):
        for path in self.file_paths:
            all_sheets = []
            file_error = ""
            wb = None
            try:
                wb = openpyxl.load_workbook(path, read_only=True)
                all_sheets = [
                    ws.title for ws in wb.worksheets if ws.sheet_state == "visible"
                ]
            except PermissionError:
                file_error = "Tệp đang bị khóa (có thể đang mở trên Excel)."
            except openpyxl.utils.exceptions.InvalidFileException:
                file_error = "Định dạng tệp không hợp lệ."
            except Exception as e:
                file_error = f"Lỗi đọc tệp: {e}"
            finally:
                if wb is not None:
                    wb.close()

            self.file_scanned.emit(path, all_sheets, file_error)

        self.finished_scan.emit()


class SheetSelectionDialog(QDialog):
    def __init__(
        self,
        file_name: str,
        all_sheets: List[str],
        selected_sheets: List[str],
        parent=None,
    ):
        super().__init__(parent)
        self.setWindowTitle(f"Chọn Sheets - {file_name}")
        self.resize(300, 400)
        layout = QVBoxLayout(self)

        lbl = QLabel("Vui lòng tích chọn các sheet cần quét:")
        layout.addWidget(lbl)

        self.list_widget = QListWidget(self)
        for sheet in all_sheets:
            item = QListWidgetItem(sheet)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(
                Qt.CheckState.Checked
                if sheet in selected_sheets
                else Qt.CheckState.Unchecked
            )
            self.list_widget.addItem(item)
        layout.addWidget(self.list_widget)

        btn_layout = QHBoxLayout()
        btn_all = QPushButton("Chọn tất cả")
        btn_none = QPushButton("Bỏ chọn tất cả")
        btn_all.clicked.connect(lambda: self._set_check_all(Qt.CheckState.Checked))
        btn_none.clicked.connect(lambda: self._set_check_all(Qt.CheckState.Unchecked))
        btn_layout.addWidget(btn_all)
        btn_layout.addWidget(btn_none)
        layout.addLayout(btn_layout)

        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def _set_check_all(self, state: Qt.CheckState):
        for i in range(self.list_widget.count()):
            self.list_widget.item(i).setCheckState(state)

    def get_selected_sheets(self) -> List[str]:
        return [
            self.list_widget.item(i).text()
            for i in range(self.list_widget.count())
            if self.list_widget.item(i).checkState() == Qt.CheckState.Checked
        ]


class TabQCCheck(QWidget):
    """
    EN: Widget for the Quality Control Check Tab.
    VI: Lớp giao diện cho Thẻ Kiểm tra Chất lượng.
    """

    scan_completed = pyqtSignal(list)  # Emits list of valid BrewRecord objects

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.qc_worker: QCWorker | None = None
        self.valid_records: List[BrewRecord] = []
        self.error_map: Dict[str, List[str]] = {}
        self.file_sheet_data: Dict[str, Dict[str, Any]] = {}
        self._setup_ui()
        self._setup_connections()

    def _setup_ui(self) -> None:
        """EN: Initialize the UI layout. VI: Khởi tạo bố cục giao diện."""
        layout = QVBoxLayout(self)

        # 1. Drag and Drop Area
        self.lbl_drop_area = QLabel(
            "📂 Kéo và thả các tệp Excel (.xlsx, .xlsm) vào đây", self
        )
        self.lbl_drop_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_drop_area.setFrameShape(QFrame.Shape.StyledPanel)
        self.lbl_drop_area.setFrameShadow(QFrame.Shadow.Sunken)
        self.lbl_drop_area.setMinimumHeight(100)
        self.lbl_drop_area.setStyleSheet("border: 2px dashed #aaa; border-radius: 5px;")
        layout.addWidget(self.lbl_drop_area)

        # 2. File List Table
        self.tbl_files = QTableWidget(0, 3, self)
        self.tbl_files.setHorizontalHeaderLabels(
            ["Tên tệp", "Sheets cần quét", "Trạng thái QC"]
        )
        header = self.tbl_files.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.tbl_files.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.tbl_files.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        layout.addWidget(self.tbl_files)

        # 3. Progress Bar and Status
        progress_layout = QHBoxLayout()
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        self.lbl_status = QLabel("Sẵn sàng kéo thả file.", self)
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.lbl_status)
        layout.addLayout(progress_layout)

        # 4. Action Buttons
        btn_layout = QHBoxLayout()
        self.btn_start_scan = QPushButton("🔬 Bắt đầu Quét QC", self)
        self.btn_clear_list = QPushButton("🧹 Xóa danh sách", self)
        self.btn_export_errors = QPushButton("📋 Xuất Log Lỗi", self)
        self.btn_start_scan.setEnabled(False)
        self.btn_export_errors.setEnabled(False)

        btn_layout.addWidget(self.btn_start_scan)
        btn_layout.addWidget(self.btn_clear_list)
        btn_layout.addWidget(self.btn_export_errors)
        layout.addLayout(btn_layout)

    def _setup_connections(self) -> None:
        """EN: Setup signal-slot connections. VI: Kết nối các tín hiệu."""
        self.btn_start_scan.clicked.connect(self._start_scan)
        self.btn_clear_list.clicked.connect(self._clear_list)
        self.btn_export_errors.clicked.connect(self._export_errors)

    # --- Drag & Drop Events ---

    def dragEnterEvent(self, event) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.lbl_drop_area.setStyleSheet(
                "border: 2px dashed #2A82DA; background-color: rgba(42, 130, 218, 0.2);"
            )
        else:
            event.ignore()

    def dragLeaveEvent(self, event) -> None:
        self.lbl_drop_area.setStyleSheet("border: 2px dashed #aaa;")

    def dropEvent(self, event) -> None:
        self.lbl_drop_area.setStyleSheet("border: 2px dashed #aaa;")
        urls = event.mimeData().urls()
        file_paths = [
            url.toLocalFile()
            for url in urls
            if url.isLocalFile()
            and url.toLocalFile().lower().endswith((".xlsx", ".xlsm"))
        ]
        if file_paths:
            self._add_files_to_table(file_paths)

    # --- Worker Slots ---

    def _update_progress(self, percentage: int, file_name: str) -> None:
        self.progress_bar.setValue(percentage)
        self.lbl_status.setText(f"Đang quét: {os.path.basename(file_name)}...")

    def _update_file_status(
        self,
        file_path: str,
        is_valid: bool,
        errors: List[str],
        data_list: List[Dict[str, Any]],
    ) -> None:
        row = self._find_row_by_path(file_path)
        if row is None:
            return

        # 1. Trích xuất và lưu dữ liệu hợp lệ (nếu có)
        if data_list:
            config = self.qc_worker.config if self.qc_worker else AppConfig()
            mappings = config.data.get("mappings", [])

            # Lấy Khóa chính dựa trên cấu hình do người dùng tích chọn (is_key)
            batch_col_letter = (
                mappings[0].get("target_col_letter", "A") if mappings else "A"
            )
            for m in mappings:
                if m.get("is_key"):
                    batch_col_letter = m.get("target_col_letter")
                    break

            for data in data_list:
                batch_val = data.get(batch_col_letter)
                if batch_val is None or str(batch_val).strip() == "":
                    import uuid

                    batch_number = f"NO_BATCH_{uuid.uuid4().hex[:6]}"
                else:
                    batch_number = str(batch_val).strip()

                self.valid_records.append(
                    BrewRecord(batch_number=batch_number, data=data)
                )

        # 2. Cập nhật UI theo 3 Trạng thái (Thành công 100%, Thành công một phần, Lỗi 100%)
        if data_list and not errors:
            status_item = QTableWidgetItem(f"✅ Đạt ({len(data_list)} mẻ)")
            status_item.setForeground(QColor(COLOR_SUCCESS_TEXT))
        elif data_list and errors:
            status_item = QTableWidgetItem(f"⚠️ Đạt ({len(data_list)} mẻ) - Có lỗi")
            status_item.setForeground(QColor("#E67E22"))  # Màu cam cảnh báo
            status_item.setToolTip("\n".join(errors))
            self.error_map[file_path] = errors
        else:
            status_item = QTableWidgetItem("❌ Lỗi")
            status_item.setForeground(QColor(COLOR_ERROR_TEXT))
            status_item.setToolTip("\n".join(errors))
            self.error_map[file_path] = errors

        self.tbl_files.setItem(row, 2, status_item)

    def _on_qc_finished(self) -> None:
        self.progress_bar.setValue(100)
        self.lbl_status.setText(
            f"Hoàn tất! {len(self.valid_records)} tệp hợp lệ, {len(self.error_map)} tệp lỗi."
        )
        self.btn_start_scan.setEnabled(True)
        self.btn_clear_list.setEnabled(True)
        if self.error_map:
            self.btn_export_errors.setEnabled(True)

        self.scan_completed.emit(self.valid_records)

    # --- Button Handlers ---

    def _start_scan(self) -> None:
        file_paths = [
            self.tbl_files.item(row, 0).text()
            for row in range(self.tbl_files.rowCount())
        ]
        if not file_paths:
            QMessageBox.warning(
                self,
                "Chưa có tệp",
                "Vui lòng kéo thả tệp vào danh sách trước khi quét.",
            )
            return

        config = AppConfig()
        fallback_name = config.data.get("fallback_profile")
        if fallback_name:
            fallback_config = AppConfig(fallback_name)
            if not fallback_config.data.get("fingerprint", "").strip():
                QMessageBox.critical(
                    self,
                    "Lỗi Bảo mật Dữ liệu",
                    f"Hồ sơ dự phòng '{fallback_name}' đang KHÔNG CÓ Dấu vân tay!\n\n"
                    f"Nếu bỏ qua, mọi file rác sẽ chui lọt vào hệ thống thông qua lỗ hổng này.\n"
                    f"Vui lòng quay lại Tab Cấu hình, mở Profile '{fallback_name}' lên và cài đặt Dấu hiệu nhận diện cho nó trước.",
                )
                return

        self.btn_start_scan.setEnabled(False)
        self.btn_clear_list.setEnabled(False)
        self.btn_export_errors.setEnabled(False)
        self.progress_bar.setValue(0)
        self.valid_records.clear()
        self.error_map.clear()

        file_sheets_map = {
            path: self.file_sheet_data.get(path, {}).get("selected", [])
            for path in file_paths
        }
        self.qc_worker = QCWorker(file_sheets_map, config)
        self.qc_worker.progress_update.connect(self._update_progress)
        self.qc_worker.file_processed.connect(self._update_file_status)
        self.qc_worker.finished.connect(self._on_qc_finished)
        self.qc_worker.start()

    def _clear_list(self) -> None:
        self.tbl_files.setRowCount(0)
        self.btn_start_scan.setEnabled(False)
        self.btn_export_errors.setEnabled(False)
        self.valid_records.clear()
        self.error_map.clear()
        self.file_sheet_data.clear()
        self.progress_bar.setValue(0)
        self.lbl_status.setText("Sẵn sàng kéo thả file.")

    def _export_errors(self) -> None:
        if not self.error_map:
            QMessageBox.information(
                self, "Không có lỗi", "Không có lỗi nào được ghi nhận để xuất."
            )
            return

        log_path = log_qc_errors(self.error_map)
        QMessageBox.information(
            self,
            "Xuất Log thành công",
            f"Đã lưu báo cáo lỗi tại:\n{os.path.abspath(log_path)}",
        )

    # --- Helper Methods ---

    def _add_files_to_table(self, file_paths: List[str]) -> None:
        current_files = {
            self.tbl_files.item(row, 0).text()
            for row in range(self.tbl_files.rowCount())
        }

        new_paths = [p for p in file_paths if p not in current_files]
        if not new_paths:
            return

        self.lbl_status.setText(f"Đang đọc danh sách sheet của {len(new_paths)} tệp...")
        self.progress_bar.setRange(0, 0)
        self.btn_start_scan.setEnabled(False)

        self.scanner_worker = FileScannerWorker(new_paths, self)
        self.scanner_worker.file_scanned.connect(self._on_file_scanned)
        self.scanner_worker.finished_scan.connect(self._on_scan_finished)
        self.scanner_worker.start()

    def _on_file_scanned(
        self, path: str, all_sheets: List[str], file_error: str
    ) -> None:
        config_sheets_str = AppConfig().data.get("input_file", {}).get("sheet_name", "")
        config_sheets = (
            [s.strip() for s in config_sheets_str.split(",")]
            if config_sheets_str
            else []
        )

        if config_sheets:
            selected_sheets = [s for s in all_sheets if s in config_sheets]
            if not selected_sheets:
                selected_sheets = all_sheets.copy()
        else:
            selected_sheets = all_sheets.copy()

        self.file_sheet_data[path] = {
            "all": all_sheets,
            "selected": selected_sheets,
        }

        self.tbl_files.setUpdatesEnabled(False)  # Khóa Render UI để tối ưu hiệu năng
        row_count = self.tbl_files.rowCount()
        self.tbl_files.insertRow(row_count)
        self.tbl_files.setItem(row_count, 0, QTableWidgetItem(path))

        if file_error:
            self.tbl_files.setItem(row_count, 1, QTableWidgetItem("N/A"))
            err_item = QTableWidgetItem(f"❌ Lỗi: Không thể đọc file")
            err_item.setForeground(QColor(COLOR_ERROR_TEXT))
            err_item.setToolTip(file_error)
            self.tbl_files.setItem(row_count, 2, err_item)
            self.error_map[path] = [file_error]
        else:
            btn_sheets = QPushButton(f"Chọn ({len(selected_sheets)}/{len(all_sheets)})")
            btn_sheets.clicked.connect(
                lambda checked, p=path, r=row_count: self._open_sheet_selector(p, r)
            )
            self.tbl_files.setCellWidget(row_count, 1, btn_sheets)
            self.tbl_files.setItem(row_count, 2, QTableWidgetItem("Chờ quét..."))

        self.tbl_files.setUpdatesEnabled(True)  # Mở lại Render UI sau khi chèn xong

    def _on_scan_finished(self) -> None:
        self.lbl_status.setText("Sẵn sàng kéo thả file.")
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        if self.tbl_files.rowCount() > 0:
            self.btn_start_scan.setEnabled(True)

    def _open_sheet_selector(self, file_path: str, row: int):
        data = self.file_sheet_data.get(file_path)
        if not data:
            return
        dialog = SheetSelectionDialog(
            os.path.basename(file_path), data["all"], data["selected"], self
        )
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data["selected"] = dialog.get_selected_sheets()
            btn = self.tbl_files.cellWidget(row, 1)
            if btn:
                btn.setText(f"Chọn ({len(data['selected'])}/{len(data['all'])})")

    def _find_row_by_path(self, file_path: str) -> int | None:
        for row in range(self.tbl_files.rowCount()):
            item = self.tbl_files.item(row, 0)
            if item and item.text() == file_path:
                return row
        return None
