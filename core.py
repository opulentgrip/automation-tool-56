import functools
import time
import collections

class ExecutionEngine:
    def __init__(self, capacity=1024):
        self.cache = collections.OrderedDict()
        self.capacity = capacity

    def memoize_crypto_math(func):
        cache = {}
        def wrapper(*args):
            if args not in cache:
                cache[args] = func(*args)
            return cache[args]
        return wrapper

    @memoize_crypto_math
    def calculate_trade_volatility(self, price_data: tuple) -> float:
        if not price_data: return 0.0
        return sum(abs(p - sum(price_data)/len(price_data)) for p in price_data) / len(price_data)

    def batch_process_signals(self, signals):
        """Vectorized-style processing for heavy crypto math operations"""
        results = []
        for signal in signals:
            start = time.perf_counter()
            val = self.calculate_trade_volatility(tuple(signal['prices']))
            results.append({'id': signal['id'], 'vol': val, 'latency': time.perf_counter() - start})
        return results

    def preallocate_memory(self, size):
        return [0.0] * size

    def __repr__(self):
        return f"Engine(cache_size={len(self.cache)}, capacity={self.capacity})"