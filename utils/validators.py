def validate_not_empty(value, field_name="Field"):
    """Ensure a value is not empty."""
    if not value or not str(value).strip():
        raise ValueError(f"{field_name} cannot be empty.")
    return True


def validate_email(email):
    """Validate email format."""
    if "@" not in email or "." not in email:
        raise ValueError("Invalid email address.")
    return True