import json
import requests
from concurrent.futures import ThreadPoolExecutor

class CryptoProcessor:
    def __init__(self, api_url):
        self.api_url = api_url

    def fetch_data(self, coin):
        response = requests.get(f'{self.api_url}/{coin}')
        return response.json() if response.status_code == 200 else None

    def process_coins(self, coins):
        results = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_coin = {executor.submit(self.fetch_data, coin): coin for coin in coins}
            for future in future_to_coin:
                coin = future_to_coin[future]
                try:
                    result = future.result()
                    if result:
                        results.append({coin: result})
                except Exception as e:
                    print(f'Error fetching {coin}: {e}')  
        return results

if __name__ == '__main__':
    processor = CryptoProcessor('https://api.coingecko.com/api/v3/simple/price')
    coins = ['bitcoin', 'ethereum', 'dogecoin']
    data = processor.process_coins(coins)
    print(json.dumps(data, indent=2))
