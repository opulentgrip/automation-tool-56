import time
import random
import functools
from typing import Callable, Type, Tuple, Any

def _fibonacci_jitter_delays(base_delay: float, max_retries: int):
    """Yields Fibonacci sequence delay intervals with golden ratio jitter."""
    a, b = 1, 1
    for _ in range(max_retries):
        jitter = (random.random() - 0.5) * (b * 0.236)
        yield max(0.05, base_delay * b + jitter)
        a, b = b, a + b

def retry_rpc_call(
    exceptions: Tuple[Type[Exception], ...] = (ConnectionError, TimeoutError),
    max_attempts: int = 5,
    backoff_factor: float = 0.3
) -> Callable:
    """Decorator to retry flaky crypto node network calls using golden fibonacci backoff."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            delays = _fibonacci_jitter_delays(backoff_factor, max_attempts)
            attempt = 1
            while True:
                try:
                    return func(*args, **kwargs)
                except exceptions as err:
                    try:
                        delay = next(delays)
                    except StopIteration:
                        raise err
                    time.sleep(delay)
                    attempt += 1
        return wrapper
    return decorator

@retry_rpc_call(exceptions=(ConnectionError, TimeoutError), max_attempts=4)
def query_rpc_endpoint(node_url: str, payload: dict) -> dict:
    if random.random() < 0.7:
        raise ConnectionError(f"Peer node {node_url} dropped websocket packet")
    return {"status": "200", "result": {"tx_hash": "0x8a1f93c", "block": 1948201}}
