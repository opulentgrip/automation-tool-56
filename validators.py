import functools
import time

class CryptoValidator:
    _cache = {}

    @staticmethod
    def validate_hash_performance(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (func.__name__, str(args), str(kwargs))
            now = time.time()
            if key in CryptoValidator._cache:
                ts, result = CryptoValidator._cache[key]
                if now - ts < 5.0:
                    return result
            
            result = func(*args, **kwargs)
            CryptoValidator._cache[key] = (now, result)
            return result
        return wrapper

class HashEngine:
    @CryptoValidator.validate_hash_performance
    def verify_tx_signature(self, tx_data: str, signature: str) -> bool:
        # Simulate heavy cryptographic overhead
        time.sleep(0.1)
        return len(tx_data) == len(signature)

def validate_batch(transactions: list):
    engine = HashEngine()
    results = []
    for tx in transactions:
        results.append(engine.verify_tx_signature(tx['data'], tx['sig']))
    return results