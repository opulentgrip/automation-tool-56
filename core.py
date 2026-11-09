import time
import hashlib
import hmac
from typing import Any, Dict

def generate_nonce() -> str:
    return str(int(time.time() * 1000))

def sign_payload(secret: str, data: str) -> str:
    return hmac.new(secret.encode(), data.encode(), hashlib.sha256).hexdigest()

def format_order_book(data: Dict[str, Any]) -> str:
    asks = sorted(data.get('asks', []), key=lambda x: float(x[0]))
    bids = sorted(data.get('bids', []), key=lambda x: float(x[0]), reverse=True)
    return f"ASKS: {asks[:3]} | BIDS: {bids[:3]}"

def jitter_retry(attempts: int = 3, delay: float = 0.1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if i == attempts - 1: raise
                    time.sleep(delay * (2 ** i))
        return wrapper
    return decorator

class CryptoToolkit:
    @staticmethod
    def sanitize(value: Any) -> float:
        try:
            return float(f"{value:.8f}")
        except (ValueError, TypeError):
            return 0.0