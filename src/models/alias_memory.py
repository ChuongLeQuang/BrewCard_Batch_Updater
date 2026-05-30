"""
EN: Memory system for alias mappings to learn from user's choices.
VI: Hệ thống bộ nhớ cho việc ghép nối tên cột, học hỏi từ lựa chọn của người dùng.
"""

import json
import os
from typing import Dict, Optional


class AliasMemory:
    """EN: Manages loading and saving user-mapped aliases. VI: Quản lý tên cột học được."""

    def __init__(self):
        self.filepath = "data/alias_memory.json"
        self.memory: Dict[str, str] = {}
        self.load()

    def load(self) -> None:
        """EN: Load memory from JSON. VI: Tải bộ nhớ từ JSON."""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    self.memory = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.memory = {}

    def save(self) -> None:
        """EN: Save memory to JSON. VI: Lưu bộ nhớ xuống JSON."""
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, indent=4, ensure_ascii=False)

    def add_alias(self, unknown_name: str, target_name: str) -> None:
        key = unknown_name.strip().lower()
        if key and target_name and target_name != "❌":
            self.memory[key] = target_name
            self.save()

    def get_target(self, unknown_name: str) -> Optional[str]:
        return self.memory.get(unknown_name.strip().lower())
