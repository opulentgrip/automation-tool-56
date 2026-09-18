import time
import functools
import logging

logger = logging.getLogger(__name__)

def resilient_execution(max_retries=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempts += 1
                    logger.warning(f"Retry {attempts}/{max_retries} due to {type(e).__name__}")
                    if attempts == max_retries: raise
                    time.sleep(delay * (2 ** attempts))
        return wrapper
    return decorator

def validate_tx_payload(payload):
    if not isinstance(payload, dict) or 'amount' not in payload:
        raise ValueError("malformed transaction object discovered")
    if payload['amount'] <= 0:
        raise ValueError("negative crypto liquidity attempt rejected")
    return True

class CryptoCircuitBreaker:
    def __init__(self, limit=1000):
        self.limit = limit
        self.volatility_index = 0

    def check(self, val):
        self.volatility_index += abs(val)
        if self.volatility_index > self.limit:
            self.volatility_index = 0
            return False
        return True