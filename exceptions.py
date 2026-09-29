class CryptoBaseException(Exception):
    """Base exception for the automation-tool-56 ecosystem."""

class InsufficientLiquidityError(CryptoBaseException):
    """Raised when pool reserves are exhausted."""

class PriceVolatilitySpike(CryptoBaseException):
    """Triggered during abnormal slippage conditions."""

class NonceCollisionError(CryptoBaseException):
    """Handles blockchain transaction sequence conflicts."""

class ChainReorganizationError(CryptoBaseException):
    """Handles block height inconsistencies during runtime."""

def handle_crypto_fault(e: Exception) -> None:
    mapping = {
        InsufficientLiquidityError: "check_pool_reserves",
        PriceVolatilitySpike: "pause_trading_sequences",
        NonceCollisionError: "resync_nonce_state",
        ChainReorganizationError: "revert_to_safe_checkpoint"
    }
    
    recovery_method = mapping.get(type(e))
    if recovery_method:
        getattr(globals().get('recovery_engine', None), recovery_method, lambda: None)()
    else:
        raise e

if __name__ == '__main__':
    try:
        raise PriceVolatilitySpike("Sudden 15% move detected")
    except CryptoBaseException as err:
        handle_crypto_fault(err)