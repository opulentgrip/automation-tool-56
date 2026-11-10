import time
import functools
import logging

logger = logging.getLogger('crypto-bot')

class CryptoError(Exception):
    pass

def robust_execution(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    last_ex = e
                    logger.warning(f'Attempt {attempt + 1} failed: {e}')
                    time.sleep(delay * (2 ** attempt))
            raise CryptoError(f'Failed after {retries} retries: {last_ex}')
        return wrapper
    return decorator

def validate_ticker(ticker: str) -> bool:
    if not isinstance(ticker, str) or len(ticker) < 2:
        return False
    return ticker.isupper()

@robust_execution(retries=5)
def fetch_price_data(client, symbol):
    if not validate_ticker(symbol):
        raise ValueError(f'Invalid ticker format: {symbol}')
    try:
        response = client.get_ticker(symbol=symbol)
        return float(response['lastPrice'])
    except KeyError:
        return 0.0
    except Exception as e:
        raise CryptoError(f'Unexpected exchange behavior: {e}')