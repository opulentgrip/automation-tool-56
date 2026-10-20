import time
import functools
from typing import Callable, Any

def retry_on_failure(max_retries: int = 3, delay: float = 1.5):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for i in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay * (2 ** i))
            raise last_ex
        return wrapper
    return decorator

class CryptoFormatter:
    @staticmethod
    def sanitize_ticker(ticker: str) -> str:
        return ticker.strip().upper().replace('/', '_')

    @staticmethod
    def format_asset_pair(base: str, quote: str) -> str:
        return f"{base.upper()}_{quote.upper()}"

def batch_process(items: list, size: int):
    """Chunking logic for API rate limit evasion."""
    for i in range(0, len(items), size):
        yield items[i:i + size]

def timestamp_now() -> int:
    return int(time.time() * 1000)

def get_environment_config(key: str, default: Any = None) -> Any:
    import os
    return os.getenv(key, default)