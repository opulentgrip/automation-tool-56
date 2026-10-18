import time
import functools
import random
import logging

logger = logging.getLogger('automation-tool-56')

class NetworkError(Exception):
    """Custom exception for crypto RPC failures."""
    pass

def retry_with_backoff(retries=3, base_delay=1.0, backoff=2.0):
    """Decorator for jittered exponential backoff retries."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            current_delay = base_delay
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except (NetworkError, ConnectionError) as e:
                    attempt += 1
                    if attempt == retries:
                        logger.error(f"Max retries reached for {func.__name__}")
                        raise e
                    sleep_time = current_delay + random.uniform(0, 0.5)
                    logger.warning(f"Retry {attempt}/{retries} after {sleep_time:.2f}s")
                    time.sleep(sleep_time)
                    current_delay *= backoff
        return wrapper
    return decorator