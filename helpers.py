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

def format_crypto(amount, precision=8):
    return f"{Decimal(str(amount)):.{precision}f}"

def sign_payload(data, secret):
    import hmac
    import hashlib
    msg = "&".join([f"{k}={v}" for k, v in sorted(data.items())])
    return hmac.new(secret.encode(), msg.encode(), hashlib.sha256).hexdigest()

class CryptoBuffer:
    def __init__(self, size=100):
        self._data = []
        self.size = size

    def push(self, item):
        self._data.append(item)
        if len(self._data) > self.size:
            self._data.pop(0)

    def get_avg(self):
        if not self._data: return 0
        return sum(self._data) / len(self._data)