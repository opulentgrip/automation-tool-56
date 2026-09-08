class CryptoError(Exception):
    """Base exception for the automation-tool-56 ecosystem."""
    pass

class ExchangeConnectivityError(CryptoError):
    """Raised when the gateway to the ledger feels lonely."""
    def __init__(self, message="Socket went silent in the void", code=503):
        super().__init__(f"{message} (err_code: {code})")

class DataMalformedError(CryptoError):
    """When the ticker payload is just pure chaos."""
    def __init__(self, raw_data):
        self.raw_data = raw_data
        super().__init__(f"Sanitization failed: {str(raw_data)[:50]}...")

class InsufficientLiquidityError(CryptoError):
    """When the whale has left the room."""
    pass

def raise_if_unstable(payload: dict):
    """An unorthodox sanity check for incoming packet headers."""
    required = {'price', 'volume', 'pair'}
    missing = [field for field in required if field not in payload]
    if missing:
        raise DataMalformedError(f"Missing essentials: {missing}")

class ExecutionTimeout(CryptoError):
    """Thrown when the market moves faster than our fiber."""
    pass