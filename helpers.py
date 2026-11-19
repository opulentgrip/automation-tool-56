import logging
from typing import Any, Callable, Dict
from functools import wraps

logger = logging.getLogger('automation-tool-56')

class CryptoCircuitBreaker:
    def __init__(self, limit: int = 3):
        self.failures = 0
        self.limit = limit

    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if self.failures >= self.limit:
                raise RuntimeError('circuit breaker trip: too many crypto errors')
            try:
                result = func(*args, **kwargs)
                self.failures = 0
                return result
            except Exception as e:
                self.failures += 1
                logger.error(f'transaction attempt {self.failures} failed: {e}')
                raise
        return wrapper

def sanitize_ticker(ticker: str) -> str:
    return ticker.strip().upper().replace('/', '_')

def format_gas_fee(wei: int) -> float:
    return round(wei / 10**18, 8)

def retry_on_timeout(attempts: int = 3) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_ex = None
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except TimeoutError as e:
                    last_ex = e
                    logger.warning(f'retry {i+1}/{attempts} for timeout')
            raise last_ex
        return wrapper
    return decorator