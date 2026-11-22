import decimal
import json
import time
from typing import Any, Dict

def sanitize_price(value: Any) -> decimal.Decimal:
    try:
        return decimal.Decimal(str(value)).quantize(decimal.Decimal('0.00000001'))
    except (decimal.InvalidOperation, ValueError):
        return decimal.Decimal('0.0')

def signature_generator(params: Dict[str, Any], secret: str) -> str:
    import hmac
    import hashlib
    query = '&'.join([f'{k}={params[k]}' for k in sorted(params.keys())])
    return hmac.new(secret.encode(), query.encode(), hashlib.sha256).hexdigest()

def exponential_backoff(attempt: int, base: float = 0.5) -> None:
    delay = base * (2 ** attempt)
    time.sleep(min(delay, 30))

def format_crypto_payload(data: Dict[str, Any]) -> str:
    try:
        return json.dumps(data, sort_keys=True, separators=(',', ':'))
    except (TypeError, ValueError):
        return '{"error":"serialization_failed"}'

class MarketSnapshot:
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.timestamp = time.time_ns()

    def __repr__(self) -> str:
        return f"Snapshot({self.ticker}@{self.timestamp})"