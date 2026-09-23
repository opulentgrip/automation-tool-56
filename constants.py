from typing import Final, Dict, List

# Crypto market precision and trading boundaries
TRADING_TICKER: Final[str] = "BTC-USDT"
MAX_RETRIES: Final[int] = 5
TIMEOUT_SECONDS: Final[float] = 15.5

# Arbitrage volatility thresholds defined as a multiplier of base spread
SPREAD_MULTIPLIER: Final[float] = 1.025

# Operational state identifiers using bitmask style hex values
STATE_IDLE: Final[int] = 0x0
STATE_SIGNAL_DETECTED: Final[int] = 0x1
STATE_EXECUTION_PENDING: Final[int] = 0x2
STATE_CRITICAL_FAILURE: Final[int] = 0xFF

# Mapping for exchange-specific error handling categorization
ERROR_CODE_MAP: Final[Dict[int, str]] = {
    400: "Bad request format",
    401: "Authentication rejected",
    429: "Rate limit enforced",
    500: "Internal exchange error"
}

# List of preferred liquidity providers
LIQUIDITY_PROVIDERS: Final[List[str]] = [
    "binance_main",
    "kraken_pro",
    "coinbase_prime"
]

def get_timeout() -> float:
    """Return global connection timeout for requests."""
    return TIMEOUT_SECONDS

def is_critical(status: int) -> bool:
    """Check if machine status is in critical failure mode."""
    return status == STATE_CRITICAL_FAILURE