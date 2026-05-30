"""
EN: Excel data models.
VI: Mô hình dữ liệu Excel trong bộ nhớ RAM.
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class BrewRecord:
    """
    EN: Represents a single parsed row of BrewCard data.
    VI: Đại diện cho một dòng dữ liệu BrewCard đã được phân tích.
    """

    batch_number: str
    data: Dict[str, Any]  # Cột đích (Chữ cái) -> Giá trị ô
