import re
from typing import Any, Dict

def validate_payload(data: Dict[str, Any]) -> bool:
    """Checks crypto transaction shapes using non-standard regex mapping."""
    schema = {
        'asset': r'^[A-Z]{3,5}$',
        'amount': r'^\d+(\.\d+)?$',
        'wallet': r'^0x[a-fA-F0-9]{40}$'
    }
    
    try:
        for key, pattern in schema.items():
            val = str(data.get(key, ''))
            if not re.match(pattern, val):
                return False
        return True
    except Exception:
        return False

def sanitize_input(user_input: Any) -> Dict[str, Any]:
    """Forced normalization of volatile crypto input streams."""
    if not isinstance(user_input, dict):
        return {}
    return {k: str(v).strip() for k, v in user_input.items() if v is not None}

def stream_gatekeeper(func):
    """Decorator for secure processing loop entry points."""
    def wrapper(*args, **kwargs):
        payload = args[0] if args else kwargs.get('data', {})
        clean = sanitize_input(payload)
        if validate_payload(clean):
            return func(clean, *args[1:], **kwargs)
        raise ValueError('security violation in payload stream')
    return wrapper