"""
EN: Unit tests for the application configuration model.
VI: Kiểm thử đơn vị cho mô hình dữ liệu cấu hình ứng dụng.
"""

import os
import json
import pytest
from src.models.config_model import AppConfig


@pytest.fixture
def temp_env(tmp_path, monkeypatch):
    """
    EN: Mock the working directory to prevent overriding real config files.
    VI: Giả lập thư mục làm việc để không ghi đè lên tệp cấu hình thật.
    """
    monkeypatch.chdir(tmp_path)
    os.makedirs("data/profiles", exist_ok=True)
    yield tmp_path


def test_app_config_create_and_save(temp_env):
    """EN: Test creating and saving a new profile. VI: Kiểm thử tạo và lưu hồ sơ mới."""
    config = AppConfig("TestProfile")
    config.data["header_row"] = "10"
    config.save()

    assert os.path.exists("data/profiles/TestProfile.json")
    with open("data/profiles/TestProfile.json", "r", encoding="utf-8") as f:
        saved_data = json.load(f)
        assert saved_data["header_row"] == "10"


def test_app_config_load(temp_env):
    """EN: Test loading an existing profile. VI: Kiểm thử tải hồ sơ đã tồn tại."""
    profile_path = "data/profiles/ExistingProfile.json"
    with open(profile_path, "w", encoding="utf-8") as f:
        json.dump({"header_row": "99", "fingerprint": "A1=Test"}, f)

    config = AppConfig("ExistingProfile")
    assert config.data["header_row"] == "99"
    assert config.data["fingerprint"] == "A1=Test"


def test_app_config_delete(temp_env):
    """EN: Test deleting a profile. VI: Kiểm thử xóa hồ sơ."""
    config = AppConfig("ToDelete")
    config.save()
    assert os.path.exists("data/profiles/ToDelete.json")

    deleted = config.delete_profile()
    assert deleted is True
    assert not os.path.exists("data/profiles/ToDelete.json")


def test_app_config_get_all_profiles(temp_env):
    """EN: Test retrieving all profiles. VI: Kiểm thử lấy danh sách toàn bộ hồ sơ."""
    AppConfig("ProfileA").save()
    AppConfig("ProfileB").save()

    profiles = AppConfig.get_all_profiles()
    assert "ProfileA" in profiles
    assert "ProfileB" in profiles
    assert profiles == ["ProfileA", "ProfileB"]
