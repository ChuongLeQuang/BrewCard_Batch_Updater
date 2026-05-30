"""
EN: Core utility functions including path resolution and I/O retries.
VI: Các hàm tiện ích lõi bao gồm xử lý đường dẫn và thử lại I/O.
"""

import os
import sys
import time
import logging
from functools import wraps

logger = logging.getLogger(__name__)


def get_project_root() -> str:
    """
    EN: Get safe project root path (handles PyInstaller).
    VI: Lấy đường dẫn gốc dự án an toàn (xử lý khi đóng gói bằng PyInstaller).
    """
    if getattr(sys, "frozen", False):
        return sys._MEIPASS
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def retry_io(retries: int = 3, delay: float = 1.0):
    """
    EN: Retry decorator for I/O operations to handle transient errors/locks.
    VI: Decorator thử lại cho các tác vụ I/O để xử lý lỗi tạm thời/tệp bị khóa.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(
                        f"Lỗi I/O (Thử lại {attempt + 1}/{retries}) tại {func.__name__}: {e}"
                    )
                    time.sleep(delay)
            logger.error(
                f"Thất bại hoàn toàn sau {retries} lần thử tại {func.__name__}"
            )
            raise last_exception

        return wrapper

    return decorator
