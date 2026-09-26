import time
import random
import functools
from typing import Callable, Any

def exponential_jitter_retry(max_attempts: int = 5, base_delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_ex = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    if attempt == max_attempts - 1:
                        break
                    sleep_time = (base_delay * (2 ** attempt)) + (random.random() * 0.1)
                    time.sleep(sleep_time)
            raise last_ex
        return wrapper
    return decorator

@exponential_jitter_retry(max_attempts=3)
def fetch_crypto_price(ticker: str) -> float:
    # Simulate volatile network state
    if random.random() < 0.7:
        raise ConnectionError(f"Node sync failure for {ticker}")
    return random.uniform(1000.0, 60000.0)

if __name__ == "__main__":
    try:
        price = fetch_crypto_price("BTC")
        print(f"Market price recovered: {price}")
    except Exception as e:
        print(f"Operation failed after retries: {e}")