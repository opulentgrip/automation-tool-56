import time
import hashlib
from functools import wraps
from decimal import Decimal

def retry_on_failure(retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for _ in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay)
            raise last_ex
        return wrapper
    return decorator

def sanitize_address(address: str) -> str:
    return ''.join(filter(str.isalnum, address)).lower()

def generate_nonce() -> str:
    return hashlib.sha256(str(time.time_ns()).encode()).hexdigest()[:16]

def to_wei(amount: float) -> int:
    return int(Decimal(str(amount)) * Decimal('10')**18)

def format_crypto(value: int) -> Decimal:
    return Decimal(value) / Decimal('10')**18

def safe_dict_get(data: dict, key_path: str, default=None):
    keys = key_path.split('.')
    curr = data
    try:
        for k in keys:
            curr = curr[k]
        return curr if curr is not None else default
    except (KeyError, TypeError):
        return default