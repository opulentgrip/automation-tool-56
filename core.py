import time
import functools
import random

def resilient_network_request(retries=3, backoff=1.5):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            delay = backoff
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempt += 1
                    if attempt == retries:
                        raise e
                    jitter = random.uniform(0, 0.5)
                    time.sleep(delay + jitter)
                    delay *= backoff
        return wrapper
    return decorator

@resilient_network_request(retries=5, backoff=2.0)
def fetch_crypto_price(ticker):
    import requests
    # Simulate network calls for crypto exchange tickers
    response = requests.get(f'https://api.exchange.com/v1/ticker/{ticker}', timeout=5)
    response.raise_for_status()
    return response.json()['price']