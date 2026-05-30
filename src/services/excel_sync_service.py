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
        """EN: Find the column letter for the batch number. VI: Tìm chữ cái của cột Số lô."""
        for m in self.mappings:
            if "batch" in m.get("target_col", "").lower():
                return m.get("target_col_letter")
        return self.mappings[0].get("target_col_letter", "A") if self.mappings else "A"

    def sync_records(self, records: List[BrewRecord]) -> bool:
        """
        EN: Sync records into the target master file (Insert/Update/Sort).
        VI: Đồng bộ danh sách dữ liệu vào file tổng (Thêm mới/Cập nhật/Sắp xếp).
        """
        try:
            # 1. Load or create workbook
            if os.path.exists(self.target_path):
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

            # 2. Load existing data from sheet into a memory map
            data_map: Dict[str, Dict[str, Any]] = {}
            header_name_to_letter = {
                m["target_col"]: m["target_col_letter"] for m in self.mappings
            }

            if ws.max_row > 1 and ws.cell(1, 1).value is not None:
                idx_to_letter_map: Dict[int, str] = {}
                for cell in ws[1]:
                    if cell.value in header_name_to_letter:
                        idx_to_letter_map[cell.column] = header_name_to_letter[
                            cell.value
                        ]

                batch_col_idx = None
                for idx, letter in idx_to_letter_map.items():
                    if letter == self.batch_col_letter:
                        batch_col_idx = idx
                        break

                if batch_col_idx:
                    for row_values in ws.iter_rows(min_row=2, values_only=True):
                        batch_num = row_values[batch_col_idx - 1]
                        if batch_num:
                            row_data = {}
                            for idx, letter in idx_to_letter_map.items():
                                if idx <= len(row_values):
                                    row_data[letter] = row_values[idx - 1]
                            data_map[str(batch_num)] = row_data

            # 3. Merge new records into the map
            for record in records:
                data_map[record.batch_number] = record.data

            # 4. Clear sheet and write everything back, sorted
            ws.delete_rows(1, ws.max_row + 1)

            sorted_mappings = sorted(
                self.mappings,
                key=lambda m: column_index_from_string(m["target_col_letter"]),
            )
            col_letter_to_idx = {
                m["target_col_letter"]: column_index_from_string(m["target_col_letter"])
                for m in sorted_mappings
            }
            col_letter_to_format = {
                m["target_col_letter"]: FORMAT_OPTIONS.get(
                    m.get("format_type", "📝 Mặc định"), "General"
                )
                for m in sorted_mappings
            }

            for mapping in sorted_mappings:
                ws.cell(
                    row=1,
                    column=col_letter_to_idx[mapping["target_col_letter"]],
                    value=mapping["target_col"],
                )

            sorted_batches = sorted(data_map.keys())
            for row_idx, batch in enumerate(sorted_batches, 2):
                record_data = data_map[batch]
                for letter, value in record_data.items():
                    if letter in col_letter_to_idx:
                        cell = ws.cell(
                            row=row_idx, column=col_letter_to_idx[letter], value=value
                        )
                        fmt = col_letter_to_format.get(letter, "General")
                        cell.number_format = fmt

            # 5. Save workbook
            wb.save(self.target_path)
            wb.close()
            return True

        except Exception:
            return False
