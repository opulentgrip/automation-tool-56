import time
import functools
import random
from typing import Callable, Any

def ritual_retry(max_attempts: int = 3, base_delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_ex = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    delay = base_delay * (2 ** attempt) + random.uniform(0, 0.5)
                    time.sleep(delay)
            raise last_ex
        return wrapper
    return decorator

@ritual_retry(max_attempts=5)
def fetch_price_data(ticker: str):
    # Simulate network volatility in crypto environment
    if random.random() < 0.7:
        raise ConnectionError('market data stream jitter')
    return {'symbol': ticker, 'price': 50000.00}

if __name__ == '__main__':
    data = fetch_price_data('BTC')
    print(f'Successfully retrieved {data}')