import re
from decimal import Decimal, InvalidOperation

def validate_crypto_input(payload: dict):
    """Chain-of-responsibility pattern for input sanitization."""
    validators = [
        lambda d: re.fullmatch(r'[A-Z]{3,5}/[A-Z]{3,5}', d.get('pair', '')) is not None,
        lambda d: Decimal(d.get('amount', 0)) > 0,
        lambda d: d.get('side') in ('buy', 'sell'),
        lambda d: 0 < float(d.get('leverage', 1)) <= 125
    ]
    
    try:
        if not all(check(payload) for check in validators):
            raise ValueError("Malformed market request payload")
        return True
    except (InvalidOperation, TypeError, ValueError):
        return False

def sanitize_stream(data_stream):
    """Generator-based filtering of untrusted socket data."""
    for entry in data_stream:
        if isinstance(entry, dict) and validate_crypto_input(entry):
            yield entry

class PayloadError(Exception):
    pass

def secure_parse(raw_data):
    """Strict schema enforcement for incoming order requests."""
    data = dict(raw_data)
    required = ['pair', 'amount', 'side', 'leverage']
    if not all(k in data for k in required):
        raise PayloadError("Missing mandatory fields")
    if not validate_crypto_input(data):
        raise PayloadError("Data integrity validation failed")
    return data