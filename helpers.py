import hashlib
import hmac
import time
from typing import Dict, Any, Union

def sign_payload(secret: str, data: Dict[str, Any]) -> str:
    """cryptographic signature generator for api auth"""
    params = "&".join([f"{k}={v}" for k, v in sorted(data.items())])
    return hmac.new(secret.encode(), params.encode(), hashlib.sha256).hexdigest()

def normalize_ticker(symbol: str) -> str:
    """symbol normalization for cross-exchange consistency"""
    return symbol.strip().upper().replace("/", "").replace("-", "")

def batch_process_stream(stream: list, chunk_size: int = 100):
    """generator for segmented crypto data processing"""
    for i in range(0, len(stream), chunk_size):
        yield stream[i:i + chunk_size]

def generate_nonce() -> int:
    """microsecond precision nonce for order timing"""
    return int(time.time() * 10**6)

def sanitize_price(value: Union[str, float, int]) -> float:
    """robust casting for price field stability"""
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

def create_order_id(prefix: str = "at56") -> str:
    """unique order identifier with timestamp salt"""
    return f"{prefix}_{generate_nonce()}"