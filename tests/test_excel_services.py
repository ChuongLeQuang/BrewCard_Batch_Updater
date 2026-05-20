"""
EN: Unit tests for Excel services.
VI: Kiểm thử đơn vị cho các dịch vụ xử lý Excel.
"""

import os
import pytest
import openpyxl
from src.services.excel_reader_service import scan_file_qc
from src.services.excel_sync_service import BrewSyncEngine
from src.models.config_model import AppConfig
from src.models.excel_data_model import BrewRecord


@pytest.fixture
def mock_config(tmp_path):
    config = AppConfig("TestProfile")
    config.data["target_file"] = {
        "path": str(tmp_path / "master.xlsx"),
        "sheet_name": "Master",
    }
    config.data["input_file"] = {"sheet_name": "InputSheet"}
    config.data["header_row"] = "1"
    config.data["mappings"] = [
        {"target_col": "Batch", "target_col_letter": "A", "source_mapping": "B2"},
        {"target_col": "Value", "target_col_letter": "B", "source_mapping": "C2"},
        {
            "target_col": "Calc",
            "target_col_letter": "C",
            "source_mapping": "C2 * 2",
        },  # Test tích hợp AST Parser
    ]
    return config


def test_scan_file_not_found(mock_config):
    is_valid, errors, data_list = scan_file_qc("fake_file.xlsx", mock_config)
    assert is_valid is False
    assert "không tồn tại" in errors[0].lower()


def test_scan_file_wrong_sheet(tmp_path, mock_config):
    file_path = tmp_path / "wrong_sheet.xlsx"
    wb = openpyxl.Workbook()
    wb.active.title = "WrongName"
    wb.save(file_path)

    is_valid, errors, data_list = scan_file_qc(str(file_path), mock_config)
    assert is_valid is False
    assert "không tìm thấy sheet" in errors[0].lower()


def test_scan_file_success(tmp_path, mock_config):
    file_path = tmp_path / "valid.xlsx"
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "InputSheet"
    ws["B2"] = "BATCH_001"
    ws["C2"] = 100
    wb.save(file_path)

    is_valid, errors, data_list = scan_file_qc(str(file_path), mock_config)
    assert is_valid is True
    assert len(errors) == 0
    data = data_list[0]
    assert data["A"] == "BATCH_001"
    assert data["B"] == 100
    assert data["C"] == 200  # Đã qua Formula Parser tính toán


def test_sync_engine_insert_update_sort(tmp_path, mock_config):
    engine = BrewSyncEngine(mock_config)
    records = [
        BrewRecord(batch_number="B002", data={"A": "B002", "B": 200, "C": 400}),
        BrewRecord(batch_number="B001", data={"A": "B001", "B": 100, "C": 200}),
    ]

    success = engine.sync_records(records)
    assert success is True

    target_path = mock_config.data["target_file"]["path"]
    assert os.path.exists(target_path)

    wb = openpyxl.load_workbook(target_path)
    ws = wb["Master"]
    assert ws["A1"].value == "Batch"  # Tự động tạo Header nếu file trống
    assert ws["A2"].value == "B001"  # Tự động Sắp xếp tăng dần
    wb.close()
