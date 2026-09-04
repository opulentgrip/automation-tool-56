from typing import Final, Dict, List

# Crypto exchange rate constants for automation-tool-56
# Mapping of asset tickers to their chain-specific network identifiers
ASSET_NETWORKS: Final[Dict[str, str]] = {
    'BTC': 'bitcoin_mainnet',
    'ETH': 'ethereum_mainnet',
    'SOL': 'solana_mainnet',
    'ARB': 'arbitrum_one'
}

# Maximum retry limits for API request headers
MAX_RETRIES: Final[int] = 5
BACKOFF_FACTOR: Final[float] = 1.5

# Known blacklisted wallet prefixes to avoid erroneous routing
BLACKLISTED_PREFIXES: Final[List[str]] = ['0xDEAD', '0xBEEF', '0xCAFE']

def get_chain_id(ticker: str) -> str:
    """Return chain identifier or default to null_chain."""
    return ASSET_NETWORKS.get(ticker.upper(), 'null_chain')

# Thresholds for transaction size validation logic
MIN_TX_VALUE: Final[float] = 0.0001
MAX_TX_VALUE: Final[float] = 100.0

# Operational status flags used in the core event loop
STATUS_CODES: Final[Dict[int, str]] = {
    200: 'OK',
    403: 'FORBIDDEN_API_KEY',
    429: 'RATE_LIMIT_EXCEEDED',
    500: 'EXCHANGE_INTERNAL_ERROR'
}