"""
EN: Unit tests for core utility functions.
VI: Kiem thu don vi cho cac ham tien ich loi.
"""

import os
import sys
import time
import pytest
from unittest.mock import patch, MagicMock
from src.utils.core_utils import get_project_root, retry_io


class TestGetProjectRoot:
    def test_returns_path_in_normal_mode(self):
        """EN: Returns a valid directory path in normal (non-frozen) mode."""
        root = get_project_root()
        assert os.path.isdir(root)

    def test_returns_meipass_when_frozen(self):
        """EN: Returns sys._MEIPASS when running as PyInstaller bundle."""
        with patch.object(sys, "frozen", True, create=True):
            with patch.object(sys, "_MEIPASS", "/tmp/fake_meipass", create=True):
                root = get_project_root()
                assert root == "/tmp/fake_meipass"


class TestRetryIO:
    def test_success_on_first_attempt(self):
        """EN: Decorated function succeeds on the first attempt."""
        call_count = 0

        @retry_io(retries=3, delay=0.01)
        def succeed():
            nonlocal call_count
            call_count += 1
            return "ok"

        result = succeed()
        assert result == "ok"
        assert call_count == 1

    def test_retries_on_failure_then_succeeds(self):
        """EN: Retries after failures, then succeeds."""
        call_count = 0

        @retry_io(retries=3, delay=0.01)
        def fail_twice_then_succeed():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise IOError("transient error")
            return "recovered"

        result = fail_twice_then_succeed()
        assert result == "recovered"
        assert call_count == 3

    def test_raises_after_all_retries_exhausted(self):
        """EN: Raises the last exception after all retries are exhausted."""
        call_count = 0

        @retry_io(retries=2, delay=0.01)
        def always_fail():
            nonlocal call_count
            call_count += 1
            raise IOError(f"attempt {call_count}")

        with pytest.raises(IOError, match="attempt 2"):
            always_fail()
        assert call_count == 2

    def test_preserves_function_name(self):
        """EN: The @wraps decorator preserves the original function name."""

        @retry_io(retries=1, delay=0.01)
        def my_function():
            pass

        assert my_function.__name__ == "my_function"
