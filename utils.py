import time
import functools
from decimal import Decimal

def retry_with_backoff(retries=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay * (2 ** i))
            raise last_ex
        return wrapper
    return decorator

def normalize_amount(amount):
    try:
        return Decimal(str(amount)).quantize(Decimal('1.00000000'))
    except Exception:
        return Decimal('0.00000000')

class ChainTicker:
    def __init__(self, mapping):
        self._map = mapping

    def __getitem__(self, key):
        return self._map.get(key.upper(), 'UNKNOWN')

    def items(self):
        return self._map.items()

def safe_env_load(env_dict, key, default):
    raw = env_dict.get(key, default)
    return raw if raw is not None else default

def generate_nonce():
    return int(time.time() * 1000)