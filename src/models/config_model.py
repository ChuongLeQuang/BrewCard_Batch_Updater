"""
EN: Application configuration model.
VI: Mô hình dữ liệu cấu hình ứng dụng.
"""

import json
import os
import re
import glob
import logging
from typing import Dict, Any, List


class AppConfig:
    """
    EN: Manages loading and saving configuration to a JSON file.
    VI: Quản lý tải và lưu cấu hình vào tệp JSON.
    """

    @staticmethod
    def _sanitize_profile_name(name: str) -> str:
        """EN: Sanitize profile name to prevent path traversal. VI: Loại bỏ ký tự nguy hiểm khỏi tên profile."""
        sanitized = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", name.strip())
        sanitized = sanitized.replace("..", "_")
        sanitized = sanitized.strip(". ")
        return sanitized if sanitized else "BrewCard"

    def __init__(self, profile_name: str = ""):
        self.config_dir = "data/profiles"
        self.settings_path = "data/app_settings.json"

        self._migrate_old_config()

        if not profile_name:
            profile_name = self._get_last_profile()

        self.profile_name = (
            self._sanitize_profile_name(profile_name) if profile_name else "BrewCard"
        )
        self.config_path = os.path.join(self.config_dir, f"{self.profile_name}.json")

        self.data: Dict[str, Any] = self._get_default_data()
        self.load()

    def _migrate_old_config(self) -> None:
        """EN: Migrate old config to multi-profile. VI: Chuyển đổi cấu hình cũ sang hệ thống mới."""
        os.makedirs(self.config_dir, exist_ok=True)
        old_path = "data/configuration.json"
        new_path = os.path.join(self.config_dir, "BrewCard.json")
        if os.path.exists(old_path):
            try:
                import shutil

                shutil.move(old_path, new_path)
                os.makedirs(os.path.dirname(self.settings_path), exist_ok=True)
                with open(self.settings_path, "w", encoding="utf-8") as f:
                    json.dump({"last_profile": "BrewCard"}, f)
            except Exception as e:
                logging.error(f"Migration error: {e}")

    def _get_default_data(self) -> Dict[str, Any]:
        return {
            "target_file": {"path": "", "sheet_name": "BrewSync"},
            "input_file": {"sheet_name": ""},
            "input_filter": {"type": "keyword", "value": "Brew"},
            "header_row": "5",
            "fingerprint": "",
            "fallback_profile": "",
            "mappings": [],
        }

    def _get_last_profile(self) -> str:
        if os.path.exists(self.settings_path):
            try:
                with open(self.settings_path, "r", encoding="utf-8") as f:
                    return json.load(f).get("last_profile")
            except (FileNotFoundError, json.JSONDecodeError, KeyError):
                pass
        return "BrewCard"

    def _save_last_profile(self) -> None:
        os.makedirs(os.path.dirname(self.settings_path), exist_ok=True)
        with open(self.settings_path, "w", encoding="utf-8") as f:
            json.dump({"last_profile": self.profile_name}, f)

    def load(self) -> None:
        """EN: Load JSON from file. VI: Tải dữ liệu từ tệp JSON."""
        self.data = self._get_default_data()
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    self.data.update(json.load(f))
            except (FileNotFoundError, json.JSONDecodeError) as e:
                logging.error(f"Failed to load config: {e}")

    def save(self) -> None:
        """EN: Save data to JSON. VI: Lưu dữ liệu xuống tệp JSON."""
        os.makedirs(self.config_dir, exist_ok=True)
        self.profile_name = self._sanitize_profile_name(self.profile_name)
        self.config_path = os.path.join(self.config_dir, f"{self.profile_name}.json")
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)
        self._save_last_profile()

    def delete_profile(self) -> bool:
        """EN: Delete current profile. VI: Xóa cấu hình hiện tại."""
        if os.path.exists(self.config_path):
            try:
                os.remove(self.config_path)
                return True
            except (FileNotFoundError, PermissionError):
                pass
        return False

    @staticmethod
    def get_all_profiles() -> List[str]:
        """EN: Get all saved profiles. VI: Lấy danh sách tất cả các cấu hình."""
        os.makedirs("data/profiles", exist_ok=True)
        profiles = []
        for file in glob.glob("data/profiles/*.json"):
            profiles.append(os.path.splitext(os.path.basename(file))[0])
        return sorted(profiles) if profiles else ["BrewCard"]
