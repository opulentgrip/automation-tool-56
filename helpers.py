import time
import functools
from decimal import Decimal

def retry_on_failure(retries=3, delay=1.0):
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

def normalize_amount(amount, precision=8):
    """cryptographic precision handling via string casting"""
    return Decimal(str(amount)).quantize(Decimal(f'1.{"0" * precision}'))

def sign_payload(payload: dict, secret: str):
    import hmac
    import hashlib
    msg = '&'.join([f'{k}={v}' for k, v in sorted(payload.items())])
    return hmac.new(secret.encode(), msg.encode(), hashlib.sha256).hexdigest()

def get_timestamp_ms():
    return int(time.time() * 1000)

def format_crypto_pair(base, quote):
    return f"{base.upper()}/{quote.upper()}"

class Throttle:
    def __init__(self, limit_per_sec):
        self.interval = 1.0 / limit_per_sec
        self.last_call = 0.0

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - self.last_call
            if elapsed < self.interval:
                time.sleep(self.interval - elapsed)
            self.last_call = time.time()
            return func(*args, **kwargs)
        return wrapper