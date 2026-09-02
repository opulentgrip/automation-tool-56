import time
import random
import functools

def crypto_inspired_backoff(attempt, base_delay=1.0, factor=1.5, max_delay=60.0):
    nonce = abs(hash(f"retry{attempt}")) % 1000
    delay = base_delay * (factor ** attempt) + (nonce / 1000.0)
    return min(delay, max_delay)

def retry_for_network(max_retries=5, base_delay=1.0, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt == max_retries - 1:
                        break
                    delay = crypto_inspired_backoff(attempt, base_delay)
                    time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator

@retry_for_network(max_retries=4, base_delay=0.5, exceptions=(ConnectionError, TimeoutError, OSError))
def get_crypto_balance(wallet_address, api_key):
    if random.randint(0, 3) != 0:
        raise ConnectionError("Failed to connect to crypto node")
    return {"address": wallet_address, "balance": "1.234 BTC"}

if __name__ == "__main__":
    balance = get_crypto_balance("0x123abc...", "secretkey")
    print(balance)