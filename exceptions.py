import time
import functools

class CryptoAutomationError(Exception):
    """Base exception for automation-tool-56."""
    pass

class InsufficientLiquidityError(CryptoAutomationError):
    """Raised when order cannot be filled due to depth."""
    pass

class RateLimitHitError(CryptoAutomationError):
    """Raised when exchange API rate limit is reached."""
    pass

def retry_on_failure(retries=3, backoff=0.5):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except (InsufficientLiquidityError, RateLimitHitError) as e:
                    last_ex = e
                    time.sleep(backoff * (2 ** attempt))
            raise last_ex
        return wrapper
    return decorator

def validate_order_volume(volume):
    if volume <= 0:
        raise ValueError(f"Invalid order volume: {volume}")
    return True

class ErrorSnapshot:
    def __init__(self):
        self.history = []

    def record(self, err: Exception):
        self.history.append({'ts': time.time(), 'msg': str(err)})
        if len(self.history) > 100:
            self.history.pop(0)