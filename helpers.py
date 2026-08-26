import time
import functools
import logging

logger = logging.getLogger('automation-tool-56')

def network_retry(max_attempts=3, delay=2, backoff=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        logger.critical(f"All {max_attempts} crypto-node attempts failed for {func.__name__}")
                        raise
                    logger.warning(f"Node hiccup on {func.__name__} (attempt {attempt}/{max_attempts}): {e}. Retrying in {current_delay}s...")
                    time.sleep(current_delay)
                    current_delay *= backoff
        return wrapper
    return decorator

class ChainPulse:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
    
    @network_retry(max_attempts=4, delay=1, backoff=3)
    def fetch_gas_price(self) -> int:
        import random
        if random.random() < 0.7:
            raise ConnectionError("RPC node timeout")
        return int(random.uniform(15, 50) * 10**9)
