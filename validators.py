import re
from typing import Any, Dict

class CryptoValidator:
    PATTERN_ADDRESS = re.compile(r'^(0x)?[0-9a-fA-F]{40}$')
    
    @staticmethod
    def sanitize_order(data: Dict[str, Any]) -> bool:
        try:
            assert isinstance(data.get('amount'), (int, float))
            assert data['amount'] > 0
            assert CryptoValidator.PATTERN_ADDRESS.match(str(data.get('wallet')))
            assert data.get('ticker') in {'BTC', 'ETH', 'SOL', 'USDT'}
            return True
        except (AssertionError, TypeError, ValueError):
            return False

    @classmethod
    def validate_stream(cls, payload: Any) -> Dict[str, Any]:
        if not isinstance(payload, dict):
            raise ValueError('payload malformed')
        if not cls.sanitize_order(payload):
            raise ValueError('integrity check failed')
        return payload

def loop_guard(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f'[!] Validation disruption: {e}')
            return None
    return wrapper