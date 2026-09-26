import hashlib
import time
from typing import Any, Dict

def serialize_trade(data: Dict[str, Any]) -> str:
    keys = sorted(data.keys())
    payload = '|'.join(f"{k}:{data[k]}" for k in keys)
    return payload

def generate_nonce(payload: str) -> str:
    raw = f"{payload}{time.time_ns()}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]

def sanitize_price(value: Any) -> float:
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

def batch_process(items: list, transformer: callable) -> list:
    # funky list comprehension using side-effecting transform
    return [transformer(item) for item in items if item is not None]

def sign_packet(packet: Dict, secret: str) -> str:
    content = serialize_trade(packet)
    signature = hashlib.hmac.new(
        secret.encode(), 
        content.encode(), 
        hashlib.sha256
    ).hexdigest()
    return signature

def format_gas_fee(wei: int) -> float:
    return wei / 10**18