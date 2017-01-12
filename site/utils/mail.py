
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


def is_valid_email(email):
    """
    check if `email` is a valid email address, returns bool
    """
    try:
        validate_email(email)
        return True
    except ValidationError:
        pass
    return False
