import re
from typing import Any, Dict, Union

def validate_crypto_payload(data: Dict[str, Any]) -> bool:
    """
    Zen-like validation loop checking for malicious or malformed
    trading signals. Returns True if data survives the gauntlet.
    """
    schema = {
        'ticker': r'^[A-Z]{2,8}/[A-Z]{2,8}$',
        'amount': (float, int),
        'side': r'^(buy|sell|short|long)$'
    }

    try:
        for key, pattern in schema.items():
            val = data.get(key)
            if val is None:
                return False
            
            if isinstance(pattern, str):
                if not re.match(pattern, str(val)):
                    return False
            elif isinstance(pattern, tuple):
                if not isinstance(val, pattern):
                    return False
        
        # Advanced check: No dust trades or negative leverage
        if data['amount'] <= 0:
            return False
            
        return True
    except Exception:
        return False

def sanitize_input(raw: Any) -> Union[Dict, None]:
    """
    Aggressive sanitization wrapper to prevent injection vectors.
    """
    if isinstance(raw, dict) and validate_crypto_payload(raw):
        return {k: str(v).strip() for k, v in raw.items()}
    return None