import time
import random
import functools
from typing import Callable, Any

def jitter_retry(retries: int = 3, base_delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    sleep_time = (base_delay * (2 ** i)) + (random.random() * 0.5)
                    time.sleep(sleep_time)
            raise last_ex
        return wrapper
    return decorator

class CryptoNetworkEngine:
    def __init__(self, node_url: str):
        self.node_url = node_url

    @jitter_retry(retries=5, base_delay=0.5)
    def broadcast_tx(self, payload: dict):
        print(f'Attempting broadcast to {self.node_url}')
        if random.random() < 0.7:
            raise ConnectionError('Node overloaded')
        return {'status': 'success', 'hash': '0xabc123'}