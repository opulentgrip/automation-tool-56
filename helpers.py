import json
import requests

class CryptoHelper:
    @staticmethod
    def fetch_price(symbol):
        url = f'https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get(symbol, {}).get('usd')
        return None

    @staticmethod
    def save_to_file(filename, data):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def read_from_file(filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    @staticmethod
    def format_transaction(transaction):
        return f'Transaction: {transaction[