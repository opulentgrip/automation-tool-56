import os
from dataclasses import dataclass
from typing import Dict, Any

@dataclass(frozen=True)
class NetworkConfig:
    RPC_URL: str = os.getenv('RPC_URL', 'https://bsc-dataseed.binance.org/')
    CHAIN_ID: int = int(os.getenv('CHAIN_ID', 56))
    GAS_BUFFER: float = 1.25

def load_provider_settings() -> Dict[str, Any]:
    return {
        'timeout': 30,
        'retries': 3,
        'headers': {'User-Agent': 'automation-tool-56/1.0.0'}
    }

class EnvironmentRegistry:
    _storage = {
        'mainnet': NetworkConfig(),
        'testnet': NetworkConfig(RPC_URL='https://data-seed-prebsc-1-s1.binance.org:8545/', CHAIN_ID=97)
    }

    @classmethod
    def get(cls, network: str) -> NetworkConfig:
        return cls._storage.get(network, cls._storage['mainnet'])

GLOBAL_SETTINGS = load_provider_settings()