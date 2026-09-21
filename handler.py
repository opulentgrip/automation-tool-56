import time
import functools
import random
import requests

def resilient_request(max_attempts=3, base_delay=1.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < max_attempts:
                try:
                    return func(*args, **kwargs)
                except (requests.exceptions.RequestException, ConnectionError) as e:
                    attempt += 1
                    if attempt == max_attempts:
                        raise e
                    # Exponential backoff with jitter for crypto api pressure
                    jitter = random.uniform(0, 0.5)
                    sleep_time = (base_delay * (2 ** (attempt - 1))) + jitter
                    time.sleep(sleep_time)
        return wrapper
    return decorator

class CryptoNetworkHandler:
    def __init__(self, session=None):
        self.session = session or requests.Session()

    @resilient_request(max_attempts=5)
    def fetch_market_data(self, endpoint: str):
        response = self.session.get(endpoint, timeout=10)
        response.raise_for_status()
        return response.json()

def get_ticker(symbol: str):
    handler = CryptoNetworkHandler()
    url = f"https://api.exchange.com/v1/ticker/{symbol}"
    return handler.fetch_market_data(url)