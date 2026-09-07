import time
import functools
import random
from typing import Callable, Any

def retry_operation(max_attempts: int = 3, base_delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_ex = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    delay = base_delay * (2 ** attempt) + random.uniform(0, 0.1)
                    time.sleep(delay)
            raise last_ex
        return wrapper
    return decorator

@retry_operation(max_attempts=5, base_delay=0.5)
def fetch_crypto_price(ticker: str) -> float:
    # Simulate volatile network state for crypto exchange
    if random.random() < 0.7:
        raise ConnectionError(f'exchange api down for {ticker}')
    return 42069.0

if __name__ == '__main__':
    print(f'price: {fetch_crypto_price("BTC")}')