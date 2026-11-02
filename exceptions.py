class CryptoAutomationError(Exception):
    """Base exception for automation-tool-56."""

class ExchangeConnectivityError(CryptoAutomationError):
    """Raised when the crypto exchange API is unreachable."""

class InsufficientBalanceError(CryptoAutomationError):
    """Raised when wallet funds fail to cover orders."""

class RateLimitExceededError(CryptoAutomationError):
    """Raised when exchange rate limits are breached."""

class InvalidSignatureError(CryptoAutomationError):
    """Raised when HMAC authentication fails."""

class OrderExecutionError(CryptoAutomationError):
    """Raised during unexpected market order failures."""

ERROR_MAP = {
    429: RateLimitExceededError,
    403: InvalidSignatureError,
    503: ExchangeConnectivityError
}

def raise_for_status_code(code: int, message: str = "Operation failed"):
    exception_cls = ERROR_MAP.get(code, CryptoAutomationError)
    raise exception_cls(f"[{code}] {message}")

if __name__ == "__main__":
    try:
        raise_for_status_code(429, "Rate limit hit")
    except RateLimitExceededError as e:
        print(f"Caught specialized exception: {e}")