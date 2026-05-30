"""
EN: QC Error Logging Utility.
VI: Tiện ích ghi log lỗi QC.
"""

import os
from datetime import datetime
from typing import Dict, List
from src.utils.core_utils import get_project_root, retry_io


@retry_io(retries=3, delay=1.0)
def log_qc_errors(errors_map: Dict[str, List[str]]) -> str:
    """
    EN: Logs QC errors to a timestamped file and returns the file path.
    VI: Ghi lại các lỗi QC vào một tệp có dấu thời gian và trả về đường dẫn tệp.
    """
    if not errors_map:
        return ""

    log_dir = os.path.join(get_project_root(), "logs")
    os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file_path = os.path.join(log_dir, f"qc_errors_{timestamp}.txt")

    with open(log_file_path, "w", encoding="utf-8") as f:
        f.write(
            f"BÁO CÁO LỖI KIỂM TRA CHẤT LƯỢNG (QC) - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        )
        f.write("=" * 80 + "\n\n")

        for file_path, errors in errors_map.items():
            f.write(f"❌ TỆP BỊ LỖI: {os.path.basename(file_path)}\n")
            for i, error in enumerate(errors, 1):
                f.write(f"  - Lỗi {i}: {error}\n")
            f.write("-" * 40 + "\n")

    return log_file_path
