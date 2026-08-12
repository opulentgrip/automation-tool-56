import requests
import time
import random

class NetworkError(Exception):
    pass

class NetworkRequest:
    def __init__(self, retries=3, delay=2):
        self.retries = retries
        self.delay = delay

    def fetch(self, url):
        for attempt in range(self.retries):
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise an error for bad status
                return response.json()
            except requests.RequestException as e:
                if attempt < self.retries - 1:
                    wait_time = self.delay + random.uniform(0, 1)
                    print(f"Attempt {attempt + 1} failed: {e}, retrying in {wait_time:.2f} seconds...")
                    time.sleep(wait_time)
                else:
                    raise NetworkError(f"All attempts failed: {e}")

# Example usage
if __name__ == '__main__':
    requester = NetworkRequest(retries=5, delay=1)
    try:
        data = requester.fetch('https://api.example.com/data')
        print(data)
    except NetworkError as ne:
        print(str(ne))