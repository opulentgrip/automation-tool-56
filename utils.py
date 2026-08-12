import time
import requests
from functools import wraps


def retry(max_attempts=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except requests.RequestException as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise e
                    time.sleep(delay)
        return wrapper
    return decorator


@retry(max_attempts=5, delay=2)
def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def main():
    data = fetch_data('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')
    print(data)


if __name__ == '__main__':
    main()