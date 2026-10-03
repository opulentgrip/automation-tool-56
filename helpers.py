import random
import time
from functools import wraps
from typing import Any, Callable, Sequence, Type


class CryptoNetworkError(Exception):
    """Base network error for crypto RPC and exchange calls."""

    pass


class RateLimitExceeded(CryptoNetworkError):
    """Triggered when exchange or node HTTP 429 occurs."""

    pass


class NodeUnresponsive(CryptoNetworkError):
    """Triggered on socket timeouts or gateway errors."""

    pass


def _fibonacci_jitter_stream(initial: float = 0.5, cap: float = 30.0):
    a, b = initial, initial
    while True:
        jitter = random.uniform(0.8, 1.3)
        yield min(cap, a * jitter)
        a, b = b, a + b


def dynamic_rpc_retry(
    retries: int = 5,
    catch_exceptions: Sequence[Type[BaseException]] = (
        CryptoNetworkError,
        ConnectionError,
        TimeoutError,
    ),
):
    """Decorator driving dynamic retry behavior via generator-based Fibonacci jitter stream."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            delays = _fibonacci_jitter_stream()
            attempt = 0

            while True:
                try:
                    return func(*args, **kwargs)
                except catch_exceptions as exc:
                    attempt += 1
                    if attempt > retries:
                        raise exc

                    delay = next(delays)
                    if isinstance(exc, RateLimitExceeded):
                        delay *= 2.0

                    time.sleep(delay)

        return wrapper

    return decorator
