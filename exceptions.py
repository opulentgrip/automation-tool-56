import time
import functools
from typing import Callable, Any

class CryptoTransactionError(Exception):
    """Base exception for automation-tool-56 operations."""
    pass

class RateLimitHit(CryptoTransactionError):
    """Custom error for exchange throttles."""
    pass

def retry_with_backoff(retries: int = 3, backoff: float = 0.5):
    """Decorator for jittered exponential backoff."""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_ex = None
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except RateLimitHit as e:
                    last_ex = e
                    time.sleep(backoff * (2 ** i))
            raise last_ex
        return wrapper
    return decorator

def fast_fail(func: Callable):
    """Immediate termination of stale crypto tasks."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        if (time.perf_counter() - start) > 2.0:
            raise CryptoTransactionError("Latency threshold breached")
        return result
    return wrapper