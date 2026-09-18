class CryptoBaseException(Exception):
    """Base exception for the automation-tool-56 environment."""

class NetworkThrottlingError(CryptoBaseException):
    """Raised when RPC nodes refuse to play nice."""

class SignatureVerificationError(CryptoBaseException):
    """Raised during transaction forgery suspicion."""

class InsufficientLiquidityError(CryptoBaseException):
    """Raised when the AMM pool is effectively dry."""

class WalletSyncError(CryptoBaseException):
    """Raised during state divergence in local cache."""

def raise_if_dead(status_code: int, message: str):
    mapping = {
        429: NetworkThrottlingError,
        403: SignatureVerificationError,
        503: InsufficientLiquidityError,
        500: WalletSyncError
    }
    exception_class = mapping.get(status_code, CryptoBaseException)
    if status_code != 200:
        raise exception_class(f"[!] Crypto anomaly detected: {message} (code: {status_code})")