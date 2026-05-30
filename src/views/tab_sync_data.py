"""
EN: Data Synchronization Tab.
VI: Phân hệ Tổng hợp và Gộp Dữ liệu.
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QPushButton,
    QProgressBar,
    QMessageBox,
)
from PyQt6.QtCore import Qt
from typing import List
from src.models.excel_data_model import BrewRecord
from src.models.config_model import AppConfig
from src.controllers.worker_threads import SyncWorker


class TabSyncData(QWidget):
    """
    EN: Widget for the Data Synchronization Tab.
    VI: Lớp giao diện cho Thẻ Tổng hợp Dữ liệu.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.valid_records: List[BrewRecord] = []
        self.sync_worker: SyncWorker | None = None
        self._setup_ui()

    def _setup_ui(self) -> None:
        """EN: Initialize the UI layout. VI: Khởi tạo bố cục giao diện."""
        layout = QVBoxLayout(self)

        self.lbl_status = QLabel(
            "Chưa có dữ liệu hợp lệ để tổng hợp. Hãy chạy QC trước.", self
        )
        self.lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_status.setStyleSheet(
            "font-size: 14px; font-weight: bold; margin: 10px;"
        )
        layout.addWidget(self.lbl_status)

        self.tbl_preview = QTableWidget(0, 2, self)
        self.tbl_preview.setHorizontalHeaderLabels(
            ["Số lô (Batch Number)", "Dữ liệu trích xuất (Preview)"]
        )
        header = self.tbl_preview.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tbl_preview)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        btn_layout = QHBoxLayout()
        self.btn_start_sync = QPushButton("🚀 Bắt đầu Tổng hợp", self)
        self.btn_start_sync.setEnabled(False)
        self.btn_start_sync.setStyleSheet(
            "background-color: #28A745; color: white; font-weight: bold; padding: 10px; font-size: 14px;"
        )
        self.btn_start_sync.clicked.connect(self._start_sync)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_start_sync)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

    def on_qc_scan_completed(self, records: List[BrewRecord]) -> None:
        """
        EN: Slot to receive valid records from the QC tab.
        VI: Slot nhận dữ liệu hợp lệ từ tab QC.
        """
        self.valid_records = records
        self.tbl_preview.setRowCount(0)

        if self.valid_records:
            self.lbl_status.setText(
                f"Sẵn sàng gộp {len(self.valid_records)} mẻ nấu vào file Tổng."
            )
            self.btn_start_sync.setEnabled(True)
            self.progress_bar.setVisible(False)
            self.progress_bar.setValue(0)

            self.tbl_preview.setUpdatesEnabled(False)
            for record in self.valid_records:
                row = self.tbl_preview.rowCount()
                self.tbl_preview.insertRow(row)

                batch_item = QTableWidgetItem(str(record.batch_number))
                batch_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                # Hiển thị tóm tắt dữ liệu sẽ được ghi
                preview_data = ", ".join(
                    [
                        f"{k}: {v}"
                        for k, v in record.data.items()
                        if str(v).strip() != ""
                    ]
                )
                data_item = QTableWidgetItem(preview_data)

                self.tbl_preview.setItem(row, 0, batch_item)
                self.tbl_preview.setItem(row, 1, data_item)
            self.tbl_preview.setUpdatesEnabled(True)
        else:
            self.lbl_status.setText(
                "Quá trình QC đã hoàn tất nhưng không có bản ghi nào hợp lệ."
            )
            self.btn_start_sync.setEnabled(False)

    def _start_sync(self) -> None:
        """EN: Start the sync process. VI: Bắt đầu quá trình đồng bộ."""
        if not self.valid_records:
            return

        self.btn_start_sync.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(
            0, 0
        )  # Chế độ vô định (Indeterminate mode) chạy qua lại
        self.lbl_status.setText(
            "Đang tiến hành đồng bộ dữ liệu, vui lòng đợi (Không tắt ứng dụng)..."
        )

        config = AppConfig()
        self.sync_worker = SyncWorker(self.valid_records, config)
        self.sync_worker.finished.connect(self._on_sync_finished)
        self.sync_worker.start()

    def _on_sync_finished(self, success: bool, message: str) -> None:
        """EN: Handle sync finished. VI: Xử lý khi đồng bộ hoàn tất."""
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(100)

        if success:
            self.lbl_status.setText("✅ Đồng bộ thành công!")
            QMessageBox.information(self, "Thành công", message)
            self.tbl_preview.setRowCount(0)
            self.valid_records.clear()
        else:
            self.lbl_status.setText("❌ Đồng bộ thất bại!")
            self.btn_start_sync.setEnabled(True)
            QMessageBox.critical(self, "Lỗi Đồng bộ", message)
