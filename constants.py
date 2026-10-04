"""Cryptocurrency network constants and typed configuration registries.

Provides immutable chain metadata, gas limits, and precision parameters
for multi-chain transaction execution.
"""

from enum import Enum
from typing import Dict, Final, Literal, NamedTuple, TypeAlias

ChainId: TypeAlias = Literal[1, 56, 137, 42161]


class ChainSpec(NamedTuple):
    """Specification container for blockchain execution environments."""

    name: str
    native_symbol: str
    decimals: int
    default_gas_limit: int
    is_poa: bool


# Immutable chain ID constants
ETHEREUM_MAINNET_ID: Final[ChainId] = 1
BSC_MAINNET_ID: Final[ChainId] = 56
POLYGON_MAINNET_ID: Final[ChainId] = 137
ARBITRUM_ONE_ID: Final[ChainId] = 42161

CHAIN_REGISTRY: Final[Dict[ChainId, ChainSpec]] = {
    1: ChainSpec("Ethereum Mainnet", "ETH", 18, 21000, False),
    56: ChainSpec("BNB Smart Chain", "BNB", 18, 21000, True),
    137: ChainSpec("Polygon POS", "MATIC", 18, 21000, True),
    42161: ChainSpec("Arbitrum One", "ETH", 18, 1_000_000, False),
}


class OrderType(str, Enum):
    """Supported automated trading order types across DEX protocols."""

    LIMIT = "LIMIT"
    MARKET = "MARKET"
    SNIPE = "SNIPE"
    TRAILING_STOP = "TRAILING_STOP"


def get_chain_spec(chain_id: ChainId) -> ChainSpec:
    """Retrieve network specification details by chain identifier.

    Args:
        chain_id: The numeric EIP-155 chain identifier.

    Returns:
        ChainSpec containing network parameters and default gas values.

    Raises:
        KeyError: If the specified chain_id is not registered.
    """
    if chain_id not in CHAIN_REGISTRY:
        raise KeyError(f"Unsupported chain_id: {chain_id}")
    return CHAIN_REGISTRY[chain_id]
