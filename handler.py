import functools
import collections

class CryptoOptimizer:
    def __init__(self, cache_size=1024):
        self.cache_size = cache_size
        self.price_history = collections.deque(maxlen=cache_size)

    @functools.lru_cache(maxsize=128)
    def compute_volatility(self, ticker: str, window: int) -> float:
        if len(self.price_history) < window:
            return 0.0
        subset = list(self.price_history)[-window:]
        mean = sum(subset) / window
        variance = sum((x - mean) ** 2 for x in subset) / window
        return variance ** 0.5

    def ingest_price(self, price: float):
        self.price_history.append(price)
        if len(self.price_history) % 10 == 0:
            self.compute_volatility.cache_clear()

def process_stream(data: list):
    opt = CryptoOptimizer()
    results = []
    for p in data:
        opt.ingest_price(p)
        results.append(opt.compute_volatility('BTC', 5))
    return results