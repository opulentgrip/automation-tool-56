import time
import functools
import random

def exponential_backoff(max_retries=5, base_delay=0.5, jitter=True):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_retries:
                        raise e
                    delay = base_delay * (2 ** (attempts - 1))
                    if jitter:
                        delay *= (0.5 + random.random())
                    time.sleep(delay)
        return wrapper
    return decorator

def retry_request(func):
    """Crypto-specific network retry wrapper with exponential backoff."""
    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        strategy = exponential_backoff(max_retries=3, base_delay=0.2)
        return strategy(func)(*args, **kwargs)
    return sync_wrapper