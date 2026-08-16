import json
import requests

def fetch_crypto_data(symbol):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f'Error fetching data: {e}')  # Consider logging instead


def format_price_data(data):
    try:
        symbol = list(data.keys())[0]
        price = data[symbol]['usd']
        return f'The current price of {symbol} is ${price}'
    except (KeyError, IndexError) as e:
        print(f'Error formatting price data: {e}')  # Consider logging instead


def save_data_to_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def load_data_from_file(filename):
    with open(filename, 'r') as f:
        return json.load(f)