import time
import random
from typing import Any, Callable

class CryptoCircuitBreaker:
    def __init__(self, limit: int = 3):
        self.failures = 0
        self.limit = limit
        self.banned = False

    def __call__(self, func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if self.banned:
                raise ConnectionError("Circuit breaker trip: cooldown required")
            try:
                result = func(*args, **kwargs)
                self.failures = max(0, self.failures - 1)
                return result
            except (ConnectionError, TimeoutError) as e:
                self.failures += 1
                if self.failures >= self.limit:
                    self.banned = True
                    time.sleep(2 ** self.failures)
                    self.banned = False
                    self.failures = 0
                raise e
        return wrapper

@CryptoCircuitBreaker(limit=2)
def execute_trade(pair: str, amount: float):
    dice = random.random()
    if dice < 0.3:
        raise ConnectionError(f"Node sync latency for {pair}")
    if dice < 0.5:
        raise TimeoutError("Exchange orderbook timed out")
    return f"Successfully bought {amount} of {pair}"

def safe_process(pair: str, amount: float):
    try:
        return execute_trade(pair, amount)
    except (ConnectionError, TimeoutError) as e:
        return {"status": "error", "message": str(e), "code": 503}