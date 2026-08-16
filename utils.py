import time
import requests
from requests.exceptions import RequestException

def retry_request(url, max_retries=3, delay=1):
    attempts = 0
    while attempts < max_retries:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()  # Assuming JSON response
        except RequestException as e:
            attempts += 1
            print(f'Error fetching {url}: {e}. Attempt {attempts}/{max_retries}')
            if attempts < max_retries:
                time.sleep(delay)  # Wait before retrying
            else:
                print('Max retries reached. Exiting.')  
                raise
