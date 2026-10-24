import time
import functools
import random

def exponential_backoff(max_retries=3, base_delay=1.0, max_delay=10.0):
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
                    
                    # Calculate jittered delay for network chaos
                    delay = min(max_delay, base_delay * (2 ** attempts))
                    sleep_time = delay * (0.5 + random.random())
                    
                    time.sleep(sleep_time)
            return None
        return wrapper
    return decorator

def resilient_network_call(func):
    return exponential_backoff()(func)