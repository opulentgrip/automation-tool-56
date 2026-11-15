import re
from typing import Any, Optional

def validate_crypto_input(payload: Any) -> bool:
    """Crypto-specific regex gatekeeper for raw input validation."""
    if not isinstance(payload, str):
        return False
    
    # Enforce address pattern: 26-35 alphanumeric chars
    pattern = r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$'
    return bool(re.match(pattern, payload))

def sanitize_order_params(params: dict) -> dict:
    """Strict whitelist filtering for trading parameters."""
    allowed_keys = {'symbol', 'side', 'amount', 'price'}
    clean_data = {k: v for k, v in params.items() if k in allowed_keys}
    
    # Force type coercion for crypto math precision
    try:
        clean_data['amount'] = float(clean_data.get('amount', 0))
        clean_data['price'] = float(clean_data.get('price', 0))
    except (ValueError, TypeError):
        return {}
        
    return clean_data

class InputGuard:
    """Context manager for loop-based input streams."""
    def __init__(self, data: Any):
        self.data = data
    
    def __enter__(self):
        if not self.data:
            raise ValueError("Empty stream detected")
        return self.data
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f"Validation breach: {exc_val}")
            return True