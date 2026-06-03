"""
EN: Worker threads for background processing.
VI: Các luồng chạy ngầm để xử lý tác vụ nền.
"""

import logging

from PyQt6.QtCore import QThread, pyqtSignal
from typing import List, Dict, Any

from src.models.config_model import AppConfig
from src.models.excel_data_model import BrewRecord
from src.services.excel_reader_service import scan_file_qc
from src.services.excel_sync_service import BrewSyncEngine


class QCWorker(QThread):
    """
    EN: Worker thread for running QC scans on multiple files.
    VI: Luồng chạy ngầm để quét QC trên nhiều tệp.
    """

    progress_update = pyqtSignal(int, str)  # percentage, current_file_name
    file_processed = pyqtSignal(
        str, bool, list, list
    )  # file_path, is_valid, errors, data_list
    finished = pyqtSignal()

    _logger = logging.getLogger(__name__)

    def __init__(
        self, file_sheets_map: Dict[str, List[str]], config: AppConfig, parent=None
    ):
        super().__init__(parent)
        self.file_sheets_map = file_sheets_map
        self.config = config

    def run(self) -> None:
        """EN: Start the QC scanning process. VI: Bắt đầu quá trình quét QC."""
        total_files = len(self.file_sheets_map)
        for i, (file_path, target_sheets) in enumerate(self.file_sheets_map.items()):
            percentage = int(((i + 1) / total_files) * 100)
            self.progress_update.emit(percentage, file_path)

            try:
                is_valid, errors, data_list = scan_file_qc(
                    file_path, self.config, target_sheets
                )
                self.file_processed.emit(file_path, is_valid, errors, data_list)
            except Exception as e:
                self._logger.error(
                    f"Unexpected error scanning '{file_path}': {e}", exc_info=True
                )
                self.file_processed.emit(
                    file_path, False, [f"Lỗi không mong đợi: {e}"], []
                )

        self.finished.emit()


class SyncWorker(QThread):
    """
    EN: Worker thread for syncing data to the master file.
    VI: Luồng chạy ngầm để đồng bộ dữ liệu vào tệp master.
    """

    finished = pyqtSignal(bool, str)  # success, message

    def __init__(self, records: List[BrewRecord], config: AppConfig, parent=None):
        super().__init__(parent)
        self.records = records
        self.config = config

    def run(self) -> None:
        """EN: Start the sync process. VI: Bắt đầu quá trình đồng bộ."""
        try:
            engine = BrewSyncEngine(self.config)
            success = engine.sync_records(self.records)
            if success:
                self.finished.emit(True, "Đồng bộ dữ liệu thành công!")
            else:
                self.finished.emit(
                    False, "Đồng bộ thất bại. Vui lòng kiểm tra lại file đích."
                )
        except PermissionError:
            self.finished.emit(
                False,
                "Tệp đích đang bị khóa. Vui lòng tắt file Master trên Excel trước khi tổng hợp!",
            )
        except Exception as e:
            self.finished.emit(False, f"Lỗi nghiêm trọng khi đồng bộ: {e}")
