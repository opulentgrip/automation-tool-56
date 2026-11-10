import time
import functools
import random

def exponential_retry(max_attempts=3, base_delay=1.0):
    """decorator for network resiliency with jitter"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise e
                    sleep_time = (base_delay * (2 ** attempts)) + (random.random() * 0.5)
                    time.sleep(sleep_time)
        return wrapper
    return decorator

def execute_with_fallback(operation, fallback, *args, **kwargs):
    """operational safety net for critical requests"""
    try:
        return operation(*args, **kwargs)
    except Exception:
        return fallback(*args, **kwargs)

class ConnectionSentinel:
    """monitor for volatile blockchain node connectivity"""
    def __init__(self, endpoint):
        self.endpoint = endpoint
    
    def ping(self):
        return True