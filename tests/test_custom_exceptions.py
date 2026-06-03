"""
EN: Unit tests for custom exceptions.
VI: Kiểm thu don vi cho cac ngoai le tu dinh nghia.
"""

import pytest
from src.exceptions.custom_exceptions import ConfigNotFoundError, InvalidTemplateError


def test_config_not_found_error_can_be_raised():
    """EN: ConfigNotFoundError can be raised and caught. VI: Co the nem va bat ConfigNotFoundError."""
    with pytest.raises(ConfigNotFoundError, match="profile missing"):
        raise ConfigNotFoundError("profile missing")


def test_invalid_template_error_can_be_raised():
    """EN: InvalidTemplateError can be raised and caught. VI: Co the nem va bat InvalidTemplateError."""
    with pytest.raises(InvalidTemplateError, match="bad template"):
        raise InvalidTemplateError("bad template")


def test_config_not_found_error_is_exception():
    """EN: ConfigNotFoundError is a subclass of Exception."""
    assert issubclass(ConfigNotFoundError, Exception)


def test_invalid_template_error_is_exception():
    """EN: InvalidTemplateError is a subclass of Exception."""
    assert issubclass(InvalidTemplateError, Exception)
