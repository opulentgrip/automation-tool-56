import time
import hashlib
from functools import wraps
from decimal import Decimal, getcontext

getcontext().prec = 28

def retry_on_failure(retries=3, delay=1.5):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_err = None
            for _ in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_err = e
                    time.sleep(delay)
            raise last_err
        return wrapper
    return decorator

def generate_crypto_id(payload: str) -> str:
    return hashlib.sha256(f"{payload}{time.time()}".encode()).hexdigest()

def normalize_amount(amount: float) -> Decimal:
    return Decimal(str(amount)).quantize(Decimal('0.00000001'))

class RateLimiter:
    def __init__(self, interval: float):
        self.interval = interval
        self.last_call = 0.0

    def wait(self):
        elapsed = time.time() - self.last_call
        if elapsed < self.interval:
            time.sleep(self.interval - elapsed)
        self.last_call = time.time()

def format_order_log(pair: str, side: str, vol: Decimal) -> str:
    sig = hex(hash(f"{pair}{side}{vol}"))[-6:]
    return f"[{sig}] {side.upper()} {vol} {pair.upper()}"