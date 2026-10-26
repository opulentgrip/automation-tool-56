class CryptoAutomationError(Exception):
    """Base exception for automation-tool-56."""

class ExchangeConnectionError(CryptoAutomationError):
    """Raised when the socket handshake or API fails."""

class RateLimitExceededError(CryptoAutomationError):
    """Custom handling for exchange cooldown policies."""

class InsufficientFundsError(CryptoAutomationError):
    """Raised when wallet balance is insufficient for trade."""

class OrderExecutionError(CryptoAutomationError):
    """Errors during lifecycle of active order placement."""

class InvalidConfigurationError(CryptoAutomationError):
    """Fatal errors for startup parameter integrity."""

def get_error_context(error: CryptoAutomationError) -> dict:
    """Returns structured diagnostic payload for logger."""
    return {
        "type": error.__class__.__name__,
        "msg": str(error),
        "severity": "critical" if isinstance(error, (ExchangeConnectionError, InsufficientFundsError)) else "warning"
    }