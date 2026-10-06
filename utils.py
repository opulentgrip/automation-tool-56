import time
import functools
import random
import logging

logger = logging.getLogger(__name__)

def resilient_request(max_retries=3, base_delay=1.0, backoff=2.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError, OSError) as e:
                    attempts += 1
                    if attempts >= max_retries:
                        logger.error(f'operation exhausted after {attempts} attempts')
                        raise e
                    
                    sleep_time = (base_delay * (backoff ** (attempts - 1))) + (random.random() * 0.5)
                    logger.warning(f'retry {attempts}/{max_retries} after {sleep_time:.2f}s due to {e}')
                    time.sleep(sleep_time)
            return None
        return wrapper
    return decorator

@resilient_request(max_retries=5, base_delay=0.5)
def fetch_price_data(endpoint):
    # Simulate crypto exchange network fluctuations
    if random.random() < 0.7:
        raise ConnectionError('exchange socket heartbeat failed')
    return {'symbol': 'BTC', 'price': 65000.0}