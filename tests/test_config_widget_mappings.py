"""
EN: Unit tests for ConfigWidgetMappings sorting logic.
VI: Kiểm thử đơn vị cho logic sắp xếp cột Excel trong lưới Mapping.
"""

import sys
import pytest
from src.views.config_widget_mappings import ConfigWidgetMappings


def test_config_widget_mappings_sorting():
    """
    EN: Test that ConfigWidgetMappings automatically sorts mapping rows by Excel column order.
    VI: Kiểm thử ConfigWidgetMappings tự động sắp xếp các dòng ánh xạ theo đúng thứ tự cột Excel.
    """
    # Khởi tạo QApplication thủ công để PyQt6 hoạt động trong môi trường test
    from PyQt6.QtWidgets import QApplication

    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    widget = ConfigWidgetMappings()
    widget.letter_to_name = {
        "B": "Column B",
        "C": "Column C",
        "M": "Column M",
        "N": "Column N",
        "Z": "Column Z",
        "AB": "Column AB",
    }

    # Đưa danh sách mapping lộn xộn vào
    raw_mappings = [
        {
            "target_col": "Column Z",
            "target_col_letter": "Z",
            "source_mapping": "1",
            "is_key": False,
            "format_type": "📝 Mặc định",
        },
        {
            "target_col": "Column B",
            "target_col_letter": "B",
            "source_mapping": "2",
            "is_key": True,
            "format_type": "📝 Mặc định",
        },
        {
            "target_col": "Column AB",
            "target_col_letter": "AB",
            "source_mapping": "3",
            "is_key": False,
            "format_type": "📝 Mặc định",
        },
        {
            "target_col": "Column M",
            "target_col_letter": "M",
            "source_mapping": "4",
            "is_key": False,
            "format_type": "📝 Mặc định",
        },
        {
            "target_col": "Column N",
            "target_col_letter": "N",
            "source_mapping": "5",
            "is_key": False,
            "format_type": "📝 Mặc định",
        },
        {
            "target_col": "Empty",
            "target_col_letter": "",
            "source_mapping": "6",
            "is_key": False,
            "format_type": "📝 Mặc định",
        },
    ]

    # Test hàm sort logic trước
    sorted_logic = widget._sort_mappings_list(raw_mappings)
    assert sorted_logic[0]["target_col_letter"] == "B"
    assert sorted_logic[1]["target_col_letter"] == "M"
    assert sorted_logic[2]["target_col_letter"] == "N"
    assert sorted_logic[3]["target_col_letter"] == "Z"
    assert sorted_logic[4]["target_col_letter"] == "AB"
    assert sorted_logic[5]["target_col_letter"] == ""

    # Test load và get mappings trên UI
    widget.load_mappings(raw_mappings)
    sorted_mappings = widget.get_mappings()

    assert sorted_mappings[0]["target_col_letter"] == "B"
    assert sorted_mappings[1]["target_col_letter"] == "M"
    assert sorted_mappings[2]["target_col_letter"] == "N"
    assert sorted_mappings[3]["target_col_letter"] == "Z"
    assert sorted_mappings[4]["target_col_letter"] == "AB"
    assert sorted_mappings[5]["target_col_letter"] == ""
