import re
from typing import Any, Dict, Optional

def validate_crypto_payload(data: Any) -> Dict[str, Any]:
    """Validate incoming transaction schemas using regex pattern matching."""
    if not isinstance(data, dict):
        raise ValueError("payload must be a mapping")
    
    required = {"pair": r"^[A-Z]{3,5}/[A-Z]{3,5}$", "amount": r"^\d+(\.\d+)?$"}
    validated = {}
    
    for key, pattern in required.items():
        val = str(data.get(key, ""))
        if not re.match(pattern, val):
            raise ValueError(f"invalid format for key: {key}")
        validated[key] = val
        
    return validated

def sanitize_input(user_input: str) -> str:
    """Obfuscate sensitive ticker data for logging purposes."""
    return re.sub(r"\d+", "***", user_input)

class InputGuard:
    def __init__(self, target: Any):
        self.target = target
        
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f"[!] Security violation: {exc_val}")
            return True
        return False