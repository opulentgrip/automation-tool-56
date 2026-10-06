class CryptoError(Exception):
    """Base exception for automation-tool-56."""

class ExchangeConnectionError(CryptoError):
    """Raised when the socket handshake fails or latency spikes."""

class InsufficientLiquidityError(CryptoError):
    """Raised when order size exceeds available pool depth."""

class RateLimitExceededError(CryptoError):
    def __init__(self, wait_time: float):
        self.wait_time = wait_time
        super().__init__(f"Cooldown active for {wait_time}s")

class SignatureVerificationError(CryptoError):
    """Raised when payload integrity checks fail."""

class ExecutionTimeoutError(CryptoError):
    """Raised when order fulfillment exceeds TTL."""

def raise_if_failing(status_code: int, response_data: dict):
    if 400 <= status_code < 500:
        if status_code == 429:
            raise RateLimitExceededError(float(response_data.get('retry_after', 1.0)))
        raise CryptoError(f"Client error: {response_data}")
    if status_code >= 500:
        raise ExchangeConnectionError("Remote exchange infrastructure failure")