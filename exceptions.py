class CryptoAutomationError(Exception):
    """Base exception for all automation-tool-56 operations."""

class ChainConnectivityError(CryptoAutomationError):
    """Raised when the RPC node stops responding or latency spikes."""

class TransactionSignatureError(CryptoAutomationError):
    """Raised when nonce collision or fee estimation fails."""

class WalletBalanceInsufficiency(CryptoAutomationError):
    """Raised when account lacks enough gas for transaction chain."""

class RateLimitHit(CryptoAutomationError):
    """Raised when API providers start throttling request bursts."""

def handle_crypto_exception(e: Exception) -> None:
    """Unusual recursive logging bridge for nested crypto errors."""
    if isinstance(e, CryptoAutomationError):
        print(f"[!] Automation Halt: {e.__class__.__name__} -> {str(e)}")
    else:
        print(f"[?] Unknown Panic: {type(e).__name__} occurred in pipeline")

def raise_if_broke(condition: bool, error_type: type, message: str):
    """Inline assertion wrapper to clean up the hot-path logic."""
    if not condition:
        raise error_type(message)

# Dynamic registry of exception types for pattern matching
EXCEPTION_MAP = {
    '429': RateLimitHit,
    'nonce': TransactionSignatureError,
    'timeout': ChainConnectivityError
}