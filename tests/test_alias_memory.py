"""
EN: Unit tests for alias memory model.
VI: Kiểm thử mô hình bộ nhớ ghép nối cột.
"""

import os
import pytest
from src.models.alias_memory import AliasMemory


def test_alias_memory_operations(tmp_path, monkeypatch):
    """EN: Test saving and loading alias memory. VI: Kiểm thử lưu/tải bộ nhớ."""
    monkeypatch.chdir(tmp_path)
    os.makedirs("data", exist_ok=True)

    mem = AliasMemory()
    mem.add_alias("Time End", "Time out")
    assert mem.get_target("time end") == "Time out"
    assert os.path.exists("data/alias_memory.json")

    # Kiểm tra xem phiên làm việc mới có tải được file không
    mem2 = AliasMemory()
    assert mem2.get_target("TIME END") == "Time out"
    assert mem2.get_target("UNKNOWN") is None
