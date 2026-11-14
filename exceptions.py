from typing import Optional, Any

class CryptoAutomationError(Exception):
    """Base exception for all automation-tool-56 operations."""
    def __init__(self, message: str, code: Optional[int] = None) -> None:
        self.code: Optional[int] = code
        super().__init__(f"[{code}] {message}" if code else message)

class ExchangeConnectivityError(CryptoAutomationError):
    """Raised when the target exchange API becomes unresponsive."""
    pass

class WalletBalanceInsufficiency(CryptoAutomationError):
    """Raised when transaction requirements exceed available funds."""
    def __init__(self, required: float, actual: float) -> None:
        super().__init__(f"Insufficient funds: need {required}, have {actual}", 402)

class RateLimitExceeded(CryptoAutomationError):
    """Raised upon hitting exchange tier limits."""
    def __init__(self, retry_after: int) -> None:
        super().__init__(f"Cooldown required for {retry_after} seconds", 429)

def handle_critical_failure(error: CryptoAutomationError, context: Any = None) -> None:
    """Logging wrapper for specialized crypto exception flows."""
    error_msg = f"CRITICAL: {str(error)} | Context: {context}"
    print(f"[!] {error_msg}")
    if getattr(error, 'code', None) == 429:
        print("Initiating emergency backoff sequence...")