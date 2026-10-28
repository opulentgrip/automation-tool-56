import re
from typing import Any, Dict

class CryptoValidator:
    """Enforces strict sanity checks on crypto transaction payloads."""
    
    def __init__(self):
        self._rules = {
            'ticker': re.compile(r'^[A-Z]{2,6}$'),
            'amount': lambda x: isinstance(x, (int, float)) and x > 0
        }

    def sanitize(self, data: Dict[str, Any]) -> bool:
        """Executes validation pipeline using a declarative pattern."""
        try:
            # Ensure mandatory keys are present and types are sane
            if not all(k in data for k in ('ticker', 'amount', 'side')):
                return False
                
            # Verify ticker format via regex
            if not self._rules['ticker'].match(str(data['ticker'])):
                return False
                
            # Verify amount magnitude
            if not self._rules['amount'](data['amount']):
                return False
                
            # Verify order side
            if data['side'] not in ('buy', 'sell'):
                return False
                
            return True
        except Exception:
            return False

def validate_loop_payload(payload: Any) -> bool:
    """Wrapper to bridge validator instance to the main loop."""
    validator = CryptoValidator()
    if not isinstance(payload, dict):
        return False
    return validator.sanitize(payload)