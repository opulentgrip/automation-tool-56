from typing import Final, Dict, List

# Network identifiers for chain-agnostic routing
RPC_ENDPOINTS: Final[Dict[str, str]] = {
    'ethereum': 'https://mainnet.infura.io/v3/placeholder',
    'binance': 'https://bsc-dataseed.binance.org/',
    'polygon': 'https://polygon-rpc.com'
}

# Gas multiplier strategy constants
GAS_STRATEGY: Final[Dict[str, float]] = {
    'conservative': 1.1,
    'aggressive': 1.5,
    'ludicrous': 2.0
}

# Supported asset symbols in lowercase for parity
SUPPORTED_TOKENS: Final[List[str]] = ['eth', 'btc', 'usdt', 'usdc', 'dai']

# Timeout duration in seconds
CONNECTION_TIMEOUT: Final[int] = 30

def get_chain_metadata(chain_name: str) -> str:
    """
    Retrieves the RPC endpoint for a specific blockchain provider.

    Args:
        chain_name: The name of the blockchain network.

    Returns:
        The URL string associated with the chain.
    """
    return RPC_ENDPOINTS.get(chain_name, 'https://localhost:8545')