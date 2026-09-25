import re
from decimal import Decimal, InvalidOperation

def validate_crypto_payload(data: dict):
    """
    strict sanity check for crypto payloads, using regex wizardry
    for ticker symbols and decimal conversion for amounts.
    """
    schema = {'ticker': r'^[A-Z]{3,5}$', 'amount': r'^[0-9]+(\.[0-9]+)?$'}
    
    for key, pattern in schema.items():
        if key not in data:
            raise ValueError(f"Missing mandatory field: {key}")
        
        if not re.match(pattern, str(data[key])):
            raise ValueError(f"Malformed data format for {key}: {data[key]}")

    try:
        amount = Decimal(data['amount'])
        if amount <= 0:
            raise ValueError("Non-positive crypto amount detected")
    except InvalidOperation:
        raise ValueError("Failed to cast amount to financial precision")

    return True

def sanitize_input(data: dict):
    """
    in-place dict sanitization to strip unwanted whitespace
    from our inbound raw packets.
    """
    for key, value in data.items():
        if isinstance(value, str):
            data[key] = value.strip()
    return data