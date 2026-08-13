import json
import requests
from datetime import datetime

class CryptoDataHandler:
    BASE_URL = 'https://api.coingecko.com/api/v3/'

    @staticmethod
    def fetch_market_data(currency: str) -> dict:
        response = requests.get(f'{CryptoDataHandler.BASE_URL}simple/price?ids=bitcoin&vs_currencies={currency}')
        response.raise_for_status()
        return response.json()

    @staticmethod
    def format_data(data: dict, currency: str) -> str:
        price = data.get('bitcoin', {}).get(currency, 'N/A')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return json.dumps({'currency': currency, 'price': price, 'timestamp': timestamp}, indent=4)

    @staticmethod
    def get_price(currency: str) -> str:
        market_data = CryptoDataHandler.fetch_market_data(currency)
        return CryptoDataHandler.format_data(market_data, currency)

# Example usage:
# handler = CryptoDataHandler()
# print(handler.get_price('usd'))