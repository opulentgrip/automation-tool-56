import json
import requests

class CryptoDataHandler:
    def __init__(self, api_url):
        self.api_url = api_url

    def fetch_data(self, currency):
        try:
            response = requests.get(f'{self.api_url}/data/{currency}')
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f'Error fetching data: {e}')
            return None

    def save_data_to_file(self, data, filename):
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    def load_data_from_file(self, filename):
        with open(filename, 'r') as file:
            return json.load(file)

    def convert_currency(self, amount, rate):
        return amount * rate

# Example usage:
# crypto_handler = CryptoDataHandler('https://api.crypto.com')
# data = crypto_handler.fetch_data('bitcoin')
# if data:
#     crypto_handler.save_data_to_file(data, 'bitcoin_data.json')