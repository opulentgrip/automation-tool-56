import time
import functools
import random
from typing import Callable, Any

def retry_crypto_request(retries: int = 3, delay: float = 1.0, backoff: float = 2.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            local_retries = retries
            current_delay = delay
            while local_retries > 0:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    local_retries -= 1
                    if local_retries == 0:
                        raise e
                    jitter = random.uniform(0, 0.1 * current_delay)
                    time.sleep(current_delay + jitter)
                    current_delay *= backoff
        return wrapper
    return decorator

@retry_crypto_request(retries=5, delay=0.5)
def fetch_price_data(ticker: str):
    # Simulate network instability for crypto exchange APIs
    if random.random() < 0.7:
        raise ConnectionError("exchange node offline")
    return {"symbol": ticker, "price": 50000.0}