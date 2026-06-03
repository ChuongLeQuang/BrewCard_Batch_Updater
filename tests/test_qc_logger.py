"""
EN: Unit tests for the QC error logging utility.
VI: Kiểm thu don vi cho tien ich ghi log loi QC.
"""

import os
import pytest
from unittest.mock import patch
from src.utils.qc_logger import log_qc_errors


def test_log_qc_errors_empty_map(tmp_path, monkeypatch):
    """EN: Empty errors_map returns empty string. VI: Map rong tra ve chuoi rong."""
    monkeypatch.chdir(tmp_path)
    result = log_qc_errors({})
    assert result == ""


def test_log_qc_errors_single_file(tmp_path, monkeypatch):
    """EN: Logs errors for a single file. VI: Ghi log loi cho mot tep."""
    monkeypatch.chdir(tmp_path)
    with patch("src.utils.qc_logger.get_project_root", return_value=str(tmp_path)):
        errors_map = {
            "/path/to/file1.xlsx": ["Missing column A", "Invalid value in B2"]
        }
        result = log_qc_errors(errors_map)

        assert result != ""
        assert os.path.exists(result)

        with open(result, "r", encoding="utf-8") as f:
            content = f.read()
        assert "file1.xlsx" in content
        assert "Missing column A" in content
        assert "Invalid value in B2" in content


def test_log_qc_errors_multiple_files(tmp_path, monkeypatch):
    """EN: Logs errors for multiple files. VI: Ghi log loi cho nhieu tep."""
    monkeypatch.chdir(tmp_path)
    with patch("src.utils.qc_logger.get_project_root", return_value=str(tmp_path)):
        errors_map = {
            "/path/to/file1.xlsx": ["Error A"],
            "/path/to/file2.xlsx": ["Error B", "Error C"],
        }
        result = log_qc_errors(errors_map)

        assert os.path.exists(result)

        with open(result, "r", encoding="utf-8") as f:
            content = f.read()
        assert "file1.xlsx" in content
        assert "file2.xlsx" in content
        assert "Error A" in content
        assert "Error B" in content
        assert "Error C" in content


def test_log_qc_errors_creates_logs_dir(tmp_path, monkeypatch):
    """EN: Creates logs directory if it does not exist. VI: Tao thu muc logs neu chua ton tai."""
    monkeypatch.chdir(tmp_path)
    with patch("src.utils.qc_logger.get_project_root", return_value=str(tmp_path)):
        errors_map = {"/path/to/file.xlsx": ["Some error"]}
        result = log_qc_errors(errors_map)

        logs_dir = os.path.join(str(tmp_path), "logs")
        assert os.path.isdir(logs_dir)
        assert result.startswith(logs_dir)
