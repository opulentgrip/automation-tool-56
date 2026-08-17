import re

class ValidationError(Exception):
    pass

def validate_address(address):
    if not isinstance(address, str):
        raise ValidationError('Address must be a string')
    if len(address) != 42:
        raise ValidationError('Address must be 42 characters long')
    if not re.match('^0x[a-fA-F0-9]{40}$', address):
        raise ValidationError('Invalid address format')
    # Further checks can be added as needed
    return True


def validate_amount(amount):
    if not isinstance(amount, (int, float)):
        raise ValidationError('Amount must be a number')
    if amount <= 0:
        raise ValidationError('Amount must be greater than zero')
    return True


def validate_transaction(address, amount):
    try:
        validate_address(address)
        validate_amount(amount)
    except ValidationError as e:
        print(f'Validation error: {e}')
        return False
    return True