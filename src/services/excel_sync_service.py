"""
EN: Excel sync service for updating Master file.
VI: Dịch vụ đồng bộ Excel để cập nhật file Tổng.
"""

import os
import openpyxl
from openpyxl.utils import column_index_from_string
from typing import List, Dict, Any
from src.models.config_model import AppConfig
from src.models.excel_data_model import BrewRecord
from src.config.constants import FORMAT_OPTIONS


class BrewSyncEngine:
    """EN: Engine handling Insert/Update logic. VI: Động cơ xử lý chèn/cập nhật."""

    def __init__(self, config: AppConfig):
        self.config = config
        self.target_path = self.config.data["target_file"]["path"]
        self.sheet_name = self.config.data["target_file"]["sheet_name"]
        self.mappings = self.config.data["mappings"]
        self.batch_col_letter = self._find_batch_column()

    def _find_batch_column(self) -> str:
        """
        EN: Find the primary key column (Explicitly marked by user).
        VI: Lấy chữ cái của cột Khóa chính (Được người dùng tích chọn).
        """
        for m in self.mappings:
            if m.get("is_key"):
                return m.get("target_col_letter")
        return self.mappings[0].get("target_col_letter", "A") if self.mappings else "A"

    def sync_records(self, records: List[BrewRecord]) -> bool:
        """
        EN: Sync records into the target master file (Insert/Update/Sort).
        VI: Đồng bộ danh sách dữ liệu vào file tổng (Thêm mới/Cập nhật/Sắp xếp).
        """
        # Xóa bỏ khối try...except chung chung để Worker Thread có thể bắt và hiển thị lỗi thực tế lên UI

        # 1. Load or create workbook
        is_new_file = not os.path.exists(self.target_path)
        if not is_new_file:
            wb = openpyxl.load_workbook(self.target_path)
            ws = (
                wb[self.sheet_name]
                if self.sheet_name in wb.sheetnames
                else wb.create_sheet(self.sheet_name)
            )
        else:
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = self.sheet_name

        # Phân tích dòng tiêu đề từ cấu hình (vd: "5" hoặc "1-3")
        header_row_val = str(self.config.data.get("header_row", "1"))
        if "-" in header_row_val:
            header_end_idx = int(header_row_val.split("-")[1])
        else:
            header_end_idx = int(header_row_val)
        data_start_row = header_end_idx + 1

        batch_col_idx = column_index_from_string(self.batch_col_letter)
        col_letter_to_idx = {
            m["target_col_letter"]: column_index_from_string(m["target_col_letter"])
            for m in self.mappings
        }
        col_letter_to_format = {
            m["target_col_letter"]: FORMAT_OPTIONS.get(
                m.get("format_type", "📝 Mặc định"), "General"
            )
            for m in self.mappings
        }

        # Tạo tự động Header nếu là file hoàn toàn mới (hoặc sheet hoàn toàn trống)
        if is_new_file or (ws.max_row <= 1 and ws.cell(1, 1).value is None):
            for m in self.mappings:
                c_idx = column_index_from_string(m["target_col_letter"])
                ws.cell(row=header_end_idx, column=c_idx, value=m.get("target_col", ""))

        # 2. Read existing mapped data (tránh xóa các dòng để bảo toàn form/logo)
        data_map: Dict[str, Dict[str, Any]] = {}
        max_data_row = data_start_row - 1

        for row in range(data_start_row, ws.max_row + 1):
            batch_val = ws.cell(row=row, column=batch_col_idx).value
            if batch_val is not None and str(batch_val).strip() != "":
                batch_str = str(batch_val).strip()
                row_data = {}
                for letter, c_idx in col_letter_to_idx.items():
                    row_data[letter] = ws.cell(row=row, column=c_idx).value
                data_map[batch_str] = row_data
                max_data_row = max(max_data_row, row)

        # 3. Merge new records into the map
        for record in records:
            batch_num = str(record.batch_number).strip()
            if batch_num not in data_map:
                data_map[batch_num] = {}
            for letter, value in record.data.items():
                data_map[batch_num][letter] = value

        # 4. Write back sorted by batch number (chỉ ghi đè giá trị, không xóa/chèn dòng)
        def batch_sort_key(b_str):
            try:
                return (0, float(b_str))
            except ValueError:
                return (1, b_str)

        sorted_batches = sorted(data_map.keys(), key=batch_sort_key)

        for i, batch in enumerate(sorted_batches):
            row_idx = data_start_row + i
            record_data = data_map[batch]

            ws.cell(row=row_idx, column=batch_col_idx, value=batch)
            for letter, c_idx in col_letter_to_idx.items():
                if letter in record_data:
                    cell = ws.cell(row=row_idx, column=c_idx, value=record_data[letter])
                    fmt = col_letter_to_format.get(letter, "General")
                    if fmt != "General":
                        cell.number_format = fmt

        # Dọn dẹp dữ liệu cũ (nếu mảng mới ngắn hơn mảng cũ, dù hiếm khi xảy ra)
        last_written_row = data_start_row + len(sorted_batches) - 1
        for row in range(last_written_row + 1, max_data_row + 1):
            for c_idx in col_letter_to_idx.values():
                ws.cell(row=row, column=c_idx, value=None)

        # 5. Save workbook
        wb.save(self.target_path)
        wb.close()
        return True
