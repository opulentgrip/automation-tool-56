import time
import random
import functools
from typing import Callable, Any

def retry_on_failure(max_attempts: int = 3, base_delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise e
                    sleep_time = (base_delay * (2 ** (attempts - 1))) + (random.random() * 0.1)
                    time.sleep(sleep_time)
        return wrapper
    return decorator

@retry_on_failure(max_attempts=5, base_delay=0.5)
def fetch_crypto_price(ticker: str) -> float:
    # Simulate volatile network state in crypto environment
    if random.random() < 0.7:
        raise ConnectionError("node synchronization lag")
    return round(random.uniform(20000, 60000), 2)

if __name__ == "__main__":
    try:
        price = fetch_crypto_price("BTC")
        print(f"current price: {price}")
    except Exception as err:
        print(f"terminal failure: {err}")