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

def to_wei(amount: float, decimals: int = 18) -> int:
    return int(Decimal(str(amount)) * (10 ** decimals))

def chunk_list(data: list, size: int):
    for i in range(0, len(data), size):
        yield data[i:i + size]

def secret_mask(key: str) -> str:
    if len(key) < 8:
        return '***'
    return f'{key[:4]}{'x' * (len(key) - 8)}{key[-4:]}'

class CryptoTimer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self
    def __exit__(self, *args):
        self.elapsed = time.perf_counter() - self.start