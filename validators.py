import re
from typing import Any, Dict, Optional

class CryptoValidator:
    """An unorthodox but performant entry-guard for processing loop data."""
    _SCHEMAS = {
        'address': re.compile(r'^(0x)?[0-9a-fA-F]{40}$'),
        'amount': lambda x: isinstance(x, (int, float)) and x > 0,
        'ticker': lambda x: isinstance(x, str) and 3 <= len(x) <= 5
    }

    def __init__(self, mode: str = 'strict'):
        self.mode = mode

    def validate(self, packet: Dict[str, Any]) -> bool:
        """Verify packet integrity using functional dispatch table."""
        try:
            checks = {
                'address': lambda v: bool(self._SCHEMAS['address'].match(str(v))),
                'amount': self._SCHEMAS['amount'],
                'ticker': self._SCHEMAS['ticker']
            }
            return all(checks[key](packet[key]) for key in packet if key in checks)
        except KeyError:
            return False

    def sanitize(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Cleanse raw inputs with regex-based filter map."""
        if not self.validate(data):
            return None
        return {k: str(v).upper() if k == 'ticker' else v for k, v in data.items()}

def main_validator_factory(config: str) -> CryptoValidator:
    """Construct validator instance for processing context."""
    return CryptoValidator(mode=config)