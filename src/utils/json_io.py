"""
EN: Shared JSON I/O helpers with safe error handling.
VI: Tiện ích đọc/ghi JSON dùng chung với xử lý lỗi an toàn.
"""

import json
import os
import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


def load_json(file_path: str, default: Optional[Any] = None) -> Any:
    """
    EN: Load JSON from *file_path*. Returns *default* on missing file or
        decode errors.
    VI: Tải dữ liệu JSON từ *file_path*. Trả về *default* nếu tệp
        không tồn tại hoặc bị lỗi giải mã.
    """
    if not os.path.exists(file_path):
        return default
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError, KeyError) as e:
        logger.error(f"Failed to load JSON from '{file_path}': {e}")
        return default


def save_json(file_path: str, data: Any) -> None:
    """
    EN: Save *data* as JSON to *file_path*, creating parent dirs if needed.
    VI: Lưu *data* dưới dạng JSON vào *file_path*, tự tạo thư mục cha nếu cần.
    """
    parent = os.path.dirname(file_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
