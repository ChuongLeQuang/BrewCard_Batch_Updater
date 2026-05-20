"""
EN: Unit tests for the Excel formula evaluator.
VI: Các bài kiểm thử đơn vị cho bộ phân dịch công thức Excel.
"""

import pytest
from unittest.mock import MagicMock
from datetime import datetime

from src.utils.formula_parser import ExcelFormulaEvaluator


class MockCell:
    """EN: Mock cell object. VI: Đối tượng cell giả."""

    def __init__(self, value):
        self.value = value


def create_mock_sheet(data: dict) -> MagicMock:
    """
    EN: Creates a mock worksheet that can be accessed like openpyxl.
    VI: Tạo một worksheet giả có thể truy cập như openpyxl.
    """
    sheet = MagicMock()

    def get_cell_value(row: int, column: int) -> any:
        # Simple conversion from col index to letter for mocking
        col_letter = chr(ord("A") + column - 1)
        coord = f"{col_letter}{row}"
        return data.get(coord)

    def cell_side_effect(row: int, column: int) -> MockCell:
        value = get_cell_value(row, column)
        return MockCell(value)

    sheet.cell.side_effect = cell_side_effect
    return sheet


# Test data for our mock sheet, based on BrewCard.json
mock_data = {
    "A1": 10,
    "A2": 20,
    "A3": 30,
    "B1": 5,
    "B2": 0,
    "C1": 2,
    "C5": 100,
    "D1": "HELLO ",
    "D2": "WORLD",
    "F13": datetime(2023, 1, 1, 23, 30),  # Time In (over midnight)
    "F19": datetime(2023, 1, 2, 0, 15),  # Time Out (next day)
    "G13": datetime(2023, 1, 1, 8, 0),  # Time In (same day)
    "G19": datetime(2023, 1, 1, 9, 30),  # Time Out (same day)
    "E78": 150,  # Kettle Full Volume
    "E83": 140,  # KO Volume
    "I71": 10,
    "I78": 20,
    "I79": 30,
    "I80": 40,
}
mock_sheet = create_mock_sheet(mock_data)


@pytest.fixture
def evaluator() -> ExcelFormulaEvaluator:
    """EN: Provides an evaluator instance. VI: Cung cấp một đối tượng evaluator."""
    return ExcelFormulaEvaluator(mock_sheet)


@pytest.mark.parametrize(
    "formula, expected",
    [
        # 1. Basic Cell References & Numbers
        ("A1", 10),
        ("=A2", 20),
        ("123.45", 123.45),
        # 2. Basic Arithmetic
        ("A1 + B1", 15),
        ("A2 - A1", 10),
        ("A1 * C1", 20),
        ("A2 / B1", 4),
        ("A1 ^ C1", 100),
        # 3. Order of Operations
        ("A1 + B1 * C1", 20),
        ("(A1 + B1) * C1", 30),
        # 4. String Operations
        ("'PREFIX-' & A1", "PREFIX-10"),
        ("D1 & D2", "HELLO WORLD"),
        # 5. Basic Functions
        ("SUM(A1, A2, A3)", 60),
        ("AVERAGE(A1, A2, A3)", 20),
        ("MIN(A1, A2, B1)", 5),
        ("MAX(A1, A2, A3)", 30),
        ("COUNT(A1, B1, D1)", 2),
        ("ABS(B1 - A1)", 5),
        # 6. Range Functions
        ("SUM(A1:A3)", 60),
        ("AVERAGE(A1:A3)", 20),
        # 7. Mixed Range and Single Cell Functions (from BrewCard.json)
        ("SUM(I71, I78:I80)", 10 + 20 + 30 + 40),
        # 8. Logic Functions
        ("IF(A1 > B1, 1, 0)", 1),
        ("IF(A1 < B1, 'YES', 'NO')", "NO"),
        ("AND(A1 > 0, B1 > 0)", True),
        ("OR(A1 > 100, B1 > 0)", True),
        ("NOT(A1 > 100)", True),
        # 9. Nested Functions & Complex Formulas (from BrewCard.json)
        ("IF(G19 >= G13, (G19 - G13) * 24 * 60, (1 + G19 - G13) * 24 * 60)", 90),
        ("IF(F19 >= F13, (F19 - F13) * 24 * 60, (1 + F19 - F13) * 24 * 60)", 45),
        ("ABS(1 - E83 / E78 - 0.08) * 100", pytest.approx(1.3333333)),
        # 10. String Functions
        ("LEFT(D2, 3)", "WOR"),
        ("RIGHT(D1, 3)", "LO "),
        ("MID(D2, 2, 3)", "ORL"),
        ("LEN(D2)", 5),
        ("TRIM(D1)", "HELLO"),
        ("UPPER('hello')", "HELLO"),
        ("LOWER(D1)", "hello "),
        ("CONCATENATE(D1, D2, '!')", "HELLO WORLD!"),
        # 11. Time Functions
        ("HOUR(F13)", 23),
        ("MINUTE(F19)", 15),
        ("SECOND(F13)", 0),
    ],
)
def test_formula_evaluation(
    evaluator: ExcelFormulaEvaluator, formula: str, expected: any
):
    """EN: Tests various valid formulas. VI: Kiểm thử các công thức hợp lệ."""
    result = evaluator.evaluate(formula)
    if isinstance(expected, float):
        assert result == pytest.approx(expected)
    else:
        assert result == expected


@pytest.mark.parametrize(
    "formula, expected_error_str",
    [
        ("A1 / B2", "#DIV/0!"),
        ("SUM(A1, D1)", "#VALUE!"),
        ("INVALID_FUNC(A1)", "#NAME?"),
        ("A1 +", "#ERROR!"),
        ("IF(A1>B1, 1)", "#ERROR!"),
    ],
)
def test_formula_errors(
    evaluator: ExcelFormulaEvaluator, formula: str, expected_error_str: str
):
    """EN: Tests formulas that should return error strings. VI: Kiểm thử các công thức trả về chuỗi lỗi."""
    assert evaluator.evaluate(formula) == expected_error_str
