"""
EN: Excel reader service for QC.
VI: Dịch vụ đọc file Excel phục vụ kiểm tra chất lượng (QC).
"""

import os
import time
import logging
import openpyxl
from openpyxl.utils.exceptions import InvalidFileException
from typing import Dict, Any, Tuple, List
from src.models.config_model import AppConfig
from src.utils.formula_parser import ExcelFormulaEvaluator
from src.utils.core_utils import retry_io

logger = logging.getLogger(__name__)


@retry_io(retries=3, delay=1.0)
def _safe_load_workbook(file_path: str, data_only: bool = True):
    """EN: Load workbook with retry mechanism. VI: Mở tệp Excel kèm cơ chế thử lại."""
    return openpyxl.load_workbook(file_path, data_only=data_only)


def _check_fingerprint(ws, rule_str: str) -> bool:
    """EN: Check if the worksheet matches the fingerprint rule. VI: Kiểm tra xem sheet có khớp dấu vân tay không."""
    if not rule_str:
        return True

    conditions = [c.strip() for c in rule_str.split("&") if c.strip()]
    if not conditions:
        return True

    for condition in conditions:
        if "=" not in condition:
            continue
        parts = condition.split("=", 1)
        cell_coord = parts[0].strip().upper()
        expected_val = parts[1].strip().lower()
        try:
            actual_val = (
                str(ws[cell_coord].value).strip().lower()
                if ws[cell_coord].value is not None
                else ""
            )
            if expected_val not in actual_val:
                return False
        except (ValueError, TypeError, AttributeError, KeyError):
            return False

    return True


def scan_file_qc(
    file_path: str, config: AppConfig, target_sheets: List[str] = None
) -> Tuple[bool, List[str], List[Dict[str, Any]]]:
    """
    EN: Scan input file, validate against config, and extract mapped values.
    VI: Quét file đầu vào, kiểm tra hợp lệ theo cấu hình, và trích xuất dữ liệu.
    Returns: (is_valid, list_of_errors, list_of_extracted_data_dicts)
    """
    errors = []
    extracted_data_list = []

    if not os.path.exists(file_path):
        errors.append(f"File không tồn tại: {file_path}")
        return False, errors, []

    try:
        start_time = time.time()
        logger.info(f"[Milestone] Bắt đầu quét file: {file_path}")

        wb = _safe_load_workbook(file_path, data_only=True)

        input_sheet_name = config.data.get("input_file", {}).get("sheet_name")
        sheets_to_scan = []

        if target_sheets is not None:
            for sn in target_sheets:
                if sn in wb.sheetnames:
                    sheets_to_scan.append(wb[sn])
                else:
                    errors.append(f"Không tìm thấy sheet '{sn}' trong tệp.")
        else:
            if not input_sheet_name:
                sheets_to_scan = [
                    ws for ws in wb.worksheets if ws.sheet_state == "visible"
                ]
            else:
                sheet_names = [s.strip() for s in input_sheet_name.split(",")]
                for sn in sheet_names:
                    if sn in wb.sheetnames:
                        sheets_to_scan.append(wb[sn])
                    else:
                        errors.append(f"Không tìm thấy sheet '{sn}' trong tệp.")

        if not sheets_to_scan and not errors:
            errors.append("Không có sheet nào hợp lệ được tìm thấy để quét.")

        for ws in sheets_to_scan:  # Lặp qua từng sheet để quét
            sheet_errors = []

            # --- Bắt đầu Logic Nhận diện Biểu mẫu (Fingerprint) ---
            active_config = config
            visited_profiles = set()
            match_found = False

            while active_config:
                profile_name = active_config.profile_name
                if profile_name in visited_profiles:
                    break  # Chống lặp vô hạn nếu người dùng cấu hình dự phòng vòng tròn
                visited_profiles.add(profile_name)

                fingerprint = active_config.data.get("fingerprint", "")
                if _check_fingerprint(ws, fingerprint):
                    match_found = True
                    break

                fallback_name = active_config.data.get("fallback_profile", "")
                if fallback_name and fallback_name != profile_name:
                    active_config = AppConfig(fallback_name)
                else:
                    break

            if not match_found:
                errors.append(
                    f"Sheet [{ws.title}] không khớp dấu vân tay của hồ sơ '{config.profile_name}' và các hồ sơ dự phòng."
                )
                continue
            # --- Kết thúc Logic Nhận diện ---

            evaluator = ExcelFormulaEvaluator(ws)
            extracted_data = {}

            for mapping in active_config.data.get("mappings", []):
                target_letter = mapping.get("target_col_letter")
                source_mapping = mapping.get("source_mapping")

                if not target_letter or not source_mapping:
                    continue

                try:
                    value = evaluator.evaluate(source_mapping)
                    extracted_data[target_letter] = value
                except (
                    SyntaxError,
                    TypeError,
                    ValueError,
                    ZeroDivisionError,
                    NameError,
                ) as e:
                    sheet_errors.append(
                        f"Sheet [{ws.title}] - Công thức '{source_mapping}': {e}"
                    )

            if sheet_errors:
                errors.extend(sheet_errors)
            else:
                extracted_data_list.append(extracted_data)

        wb.close()

        end_time = time.time()
        logger.info(
            f"[Milestone] Hoàn tất trích xuất '{file_path}' trong {end_time - start_time:.2f} giây."
        )

    except PermissionError:
        errors.append(
            f"Tệp đang bị khóa (có thể đang mở trên Excel): {os.path.basename(file_path)}"
        )
    except InvalidFileException as e:
        errors.append(f"Định dạng tệp không hợp lệ: {e}")
    except (OSError, FileNotFoundError) as e:
        errors.append(f"Không thể đọc file Excel '{os.path.basename(file_path)}': {e}")

    # Chỉ trả về False nếu không có mẻ nào được trích xuất thành công
    if not extracted_data_list:
        return (
            False,
            (
                errors
                if errors
                else ["Không trích xuất được dữ liệu từ bất kỳ sheet nào."]
            ),
            [],
        )

    return True, errors, extracted_data_list
