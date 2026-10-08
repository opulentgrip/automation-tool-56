import time
import functools
import logging
from typing import Callable, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('automation-tool-56')

class CryptoCircuitBreaker:
    def __init__(self, retries: int = 3, delay: float = 1.5):
        self.retries = retries
        self.delay = delay

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_ex = None
            for attempt in range(self.retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    logger.warning(f'attempt {attempt + 1} failed: {e}')
                    time.sleep(self.delay * (attempt + 1))
            raise last_ex
        return wrapper

def sanitize_ticker(symbol: str) -> str:
    return symbol.upper().replace('/', '_').strip()

def format_crypto_amount(val: float, precision: int = 8) -> str:
    return f'{val:.{precision}f}'.rstrip('0').rstrip('.')

def get_timestamp() -> int:
    return int(time.time() * 1000)

def retry_on_failure(retries: int = 3) -> CryptoCircuitBreaker:
    return CryptoCircuitBreaker(retries=retries)