import time
import functools
import random
import logging

logger = logging.getLogger('automation-tool-56')

def retry_crypto_request(max_attempts=3, base_delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    jitter = random.uniform(0, 0.5)
                    sleep_time = (base_delay * (2 ** attempts)) + jitter
                    logger.warning(f'Network wobble: {e}. Retry {attempts}/{max_attempts} in {sleep_time:.2f}s')
                    if attempts >= max_attempts:
                        raise
                    time.sleep(sleep_time)
        return wrapper
    return decorator

@retry_crypto_request(max_attempts=5)
def fetch_price_data(ticker):
    # Simulate volatile crypto endpoint interaction
    if random.random() < 0.7:
        raise ConnectionError('Exchange node synchronization lag')
    return {'ticker': ticker, 'price': random.uniform(30000, 60000)}