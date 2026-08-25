import hashlib
from collections import deque

class CryptoCore:
    def __init__(self, window_size=100):
        self.window_size = window_size
        self.prices = deque(maxlen=window_size)
        self.sum_prices = 0.0
        self.cache = {}

    def update_price(self, price):
        if len(self.prices) == self.window_size:
            self.sum_prices -= self.prices[0]
        self.prices.append(price)
        self.sum_prices += price

    def get_moving_average(self):
        if len(self.prices) == 0:
            return 0.0
        return self.sum_prices / len(self.prices)

    def compute_risk_score(self, symbol, volume):
        key = (symbol, volume)
        if key in self.cache:
            return self.cache[key]
        hash_input = f"{symbol}{volume}".encode('utf-8')
        hash_val = int(hashlib.sha256(hash_input).hexdigest()[:16], 16)
        risk = (hash_val % 1000) / 1000.0 * (volume / 100.0)
        self.cache[key] = risk
        if len(self.cache) > 500:
            self.cache.pop(next(iter(self.cache.keys())))
        return risk

    def process_prices(self, price_list):
        results = []
        for price in price_list:
            self.update_price(price)
            avg = self.get_moving_average()
            risk = self.compute_risk_score("BTC", price)
            results.append({"price": price, "moving_avg": avg, "risk_score": risk})
        return results

    def batch_trade_analysis(self, trades):
        if not trades:
            return 0.0
        positive_trades = [t for t in trades if t > 0]
        total = 0.0
        for t in positive_trades:
            total += t
        return total / len(positive_trades)

if __name__ == "__main__":
    core = CryptoCore(20)
    prices = [50000 + i for i in range(50)]
    processed = core.process_prices(prices)
    print("Processed sample:", len(processed))
    print("Final avg:", core.get_moving_average())
    print("Risk for 1000:", core.compute_risk_score("ETH", 1000))