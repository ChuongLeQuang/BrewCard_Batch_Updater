"""
EN: Shared validation helpers.
VI: Tiện ích kiểm tra dữ liệu dùng chung.
"""

from typing import Optional, Tuple

from src.models.config_model import AppConfig


def validate_fallback_fingerprint(
    config: AppConfig,
) -> Tuple[bool, Optional[str]]:
    """
    EN: Check that the fallback profile (if any) has a non-empty fingerprint.
    VI: Kiểm tra rằng hồ sơ dự phòng (nếu có) phải khai báo dấu vân tay.

    Returns:
        (True, None)  if valid or no fallback is configured.
        (False, fallback_name) if the fallback has an empty fingerprint.
    """
    fallback_name = config.data.get("fallback_profile")
    if not fallback_name:
        return True, None

    fallback_config = AppConfig(fallback_name)
    if not fallback_config.data.get("fingerprint", "").strip():
        return False, fallback_name

    return True, None
