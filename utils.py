import time
import functools
import random
from typing import Callable, Any

def jitter_retry(attempts: int = 3, base_delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_ex = None
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    wait = base_delay * (2 ** i) + random.uniform(0, 0.5)
                    time.sleep(wait)
            raise last_ex
        return wrapper
    return decorator

@jitter_retry(attempts=5, base_delay=0.5)
def fetch_price_data(endpoint: str):
    # Simulate network instability for crypto API calls
    import random
    if random.random() < 0.7:
        raise ConnectionError("Exchange node timeout")
    return {"status": "success", "price": 50000.0}