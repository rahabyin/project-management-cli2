import re


def validate_not_empty(value, field_name):
    if value is None or str(value).strip() == "":
        raise ValueError(f"{field_name} cannot be empty")
    return True


def validate_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if not re.match(pattern, email):
        raise ValueError("Invalid email address")

    return True