import re
from marshmallow import ValidationError


def required(value):
    """Validate that field under validation does not contain null value."""

    if isinstance(value, str):
        if not value.strip(' '):
            raise ValidationError('The parameter cannot be null')

        return value
    elif value:
        return value


def email(value):
    """Validate field matches email format."""

    if not re.match(r"(^[a-zA-z0-9_.]+@[a-zA-z0-9-]+\.[a-z]+$)", value):
        raise ValidationError('The parameter must be a valid email')

    return value


def verifyStatus(value):
    """Validate status matches the required statuses"""

    if isinstance(value, str):
        if not value.strip(' '):
            raise ValidationError('Status cannot be null')

    statuses = ['resolved', 'rejected', 'under investigation', 'draft']

    if value not in statuses:
        raise ValidationError(
            'The status can only be resolved, rejected, under investigation or draft')

    return value


def verifyType(value):
    """Validate type matches the required types"""

    if isinstance(value, str):
        if not value.strip(' '):
            raise ValidationError('Record type cannot be null')

    types = ['red-flag', 'intervention']

    if value not in types:
        raise ValidationError(
            'The record type can only be red-flag and intervention')

    return value
