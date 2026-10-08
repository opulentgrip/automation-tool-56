import re
from typing import Any, Dict

class AddressValidator:
    _rules = {
        'btc': r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$',
        'eth': r'^0x[a-fA-F0-9]{40}$',
        'sol': r'^[1-9A-HJ-NP-Za-km-z]{32,44}$'
    }

    def __init__(self, asset_map: Dict[str, str] = None):
        self.patterns = {**self._rules, **(asset_map or {})}

    def validate(self, address: str, ticker: str) -> bool:
        pattern = self.patterns.get(ticker.lower())
        return bool(re.match(pattern, address)) if pattern else False

    @staticmethod
    def sanity_check(payload: Dict[str, Any]) -> bool:
        required = {'address', 'amount', 'ticker'}
        return all(key in payload for key in required) and float(payload['amount']) > 0

def sanitize_input(data: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v.strip() if isinstance(v, str) else v for k, v in data.items()}

validator = AddressValidator()