import time
import functools
from decimal import Decimal

def retry_on_failure(retries=3, delay=1.5):
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

def normalize_amount(value, precision=8):
    return Decimal(str(value)).quantize(Decimal('1.' + '0' * precision))

def format_trade_log(symbol, side, price, qty):
    return f"[{symbol.upper()}] {side.upper()} @ {price} | VOL: {qty}"

def crypto_throttle(limit_per_second):
    interval = 1.0 / limit_per_second
    def decorator(func):
        last_called = [0.0]
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            if elapsed < interval:
                time.sleep(interval - elapsed)
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        return wrapper
    return decorator