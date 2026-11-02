
from app.utils.validators import validate_password, normalize_email


def test_valid_password():
    valid, message = validate_password("FoodBridge123")
    assert valid is True
    assert message == ""


def test_password_too_short():
    valid, message = validate_password("Ab1")
    assert valid is False
    assert "8 characters" in message


def test_password_requires_uppercase():
    valid, message = validate_password("foodbridge123")
    assert valid is False
    assert "uppercase" in message


def test_email_normalization():
    assert normalize_email("  DONOR@Example.COM ") == "donor@example.com"


def test_empty_email():
    assert normalize_email("") == ""
