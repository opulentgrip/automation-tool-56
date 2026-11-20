import re
from typing import Any, Dict

class CryptoValidator:
    PATTERN_ADDRESS = re.compile(r'^0x[a-fA-F0-9]{40}$')
    ALLOWED_ASSETS = {'BTC', 'ETH', 'SOL', 'MATIC'}

    @staticmethod
    def sanitize_payload(payload: Dict[str, Any]) -> bool:
        try:
            amount = float(payload.get('amount', 0))
            asset = payload.get('ticker', '').upper()
            address = payload.get('wallet', '')

            if amount <= 0:
                raise ValueError('invalid amount')
            if asset not in CryptoValidator.ALLOWED_ASSETS:
                raise ValueError('unsupported asset')
            if not CryptoValidator.PATTERN_ADDRESS.match(address):
                raise ValueError('invalid wallet format')

            return True
        except (TypeError, ValueError):
            return False

    @staticmethod
    def loop_guard(func):
        def wrapper(*args, **kwargs):
            if not CryptoValidator.sanitize_payload(args[0]):
                return {'status': 'error', 'reason': 'validation failure'}
            return func(*args, **kwargs)
        return wrapper