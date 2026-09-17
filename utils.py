import time
import decimal
from functools import wraps

def retry_on_failure(retries=3, delay=1.0):
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

def format_crypto(value: float, precision: int = 8) -> str:
    ctx = decimal.Context(prec=precision)
    return str(ctx.create_decimal(repr(value)).normalize())

def sign_payload(payload: dict, secret: str) -> str:
    import hashlib
    import hmac
    encoded = '&'.join([f'{k}={v}' for k, v in sorted(payload.items())])
    return hmac.new(secret.encode(), encoded.encode(), hashlib.sha256).hexdigest()

def timestamp_ms() -> int:
    return int(time.time() * 1000)

def sanitize_order(order: dict) -> dict:
    return {k: v for k, v in order.items() if v is not None}