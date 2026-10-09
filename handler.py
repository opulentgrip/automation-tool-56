import time
import random
from typing import Any, Callable

class CryptoError(Exception):
    pass

class ResilienceHandler:
    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries
        self.backoff_factor = 0.5

    def execute(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        attempts = 0
        while attempts < self.max_retries:
            try:
                return func(*args, **kwargs)
            except (ConnectionError, TimeoutError) as e:
                attempts += 1
                if attempts >= self.max_retries:
                    raise CryptoError(f"Final failure after {attempts} attempts: {e}")
                sleep_time = (self.backoff_factor * (2 ** attempts)) + (random.random() * 0.1)
                time.sleep(sleep_time)
            except Exception as e:
                raise CryptoError(f"Fatal non-recoverable error encountered: {type(e).__name__}") from e

def validate_wallet_address(address: str) -> bool:
    if not isinstance(address, str) or len(address) < 26:
        raise ValueError("Invalid blockchain address format")
    return True

# Usage example for the engine
if __name__ == '__main__':
    handler = ResilienceHandler()
    safe_task = lambda: "0xSuccess" if random.random() > 0.2 else exec("raise(ConnectionError('RPC Fail'))")
    result = handler.execute(safe_task)
    print(f"Operation output: {result}")