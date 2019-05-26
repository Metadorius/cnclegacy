import re
from wtforms import ValidationError

def password_validator(form, field):
    if not re.match("^[a-z0-9_-]{6,}$", field.data, flags=re.IGNORECASE):
        raise ValidationError("Password can't be shorter than 6 symbols or contain characters other than a-z, 0-9, underscore or hyphen!")

def username_validator(form, field):
    if not re.match("^[a-z0-9_-]{3,}$", field.data, flags=re.IGNORECASE):
        raise ValidationError("Username can't be shorter than 3 symbols or contain characters other than a-z, 0-9, underscore or hyphen!")

def slug_validator(form, field):
    if not re.match("^[a-z0-9-]+$", field.data):
        raise ValidationError("URL slug can't contain characters other than a-z, 0-9 or hyphen!")
