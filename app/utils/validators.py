
import re


def validate_password(password):
    """Require a strong password for new accounts."""
    if not password or len(password) < 8:
        return False, "Password must contain at least 8 characters."

    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."

    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."

    if not re.search(r"\d", password):
        return False, "Password must contain at least one number."

    return True, ""


def normalize_email(email):
    """Normalize an email address before storing or searching for it."""
    return email.strip().lower() if email else ""
