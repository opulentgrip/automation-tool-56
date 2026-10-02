import os
from typing import Dict, Any
from dataclasses import dataclass

@dataclass(frozen=True)
class NetworkSettings:
    rpc_url: str
    chain_id: int
    gas_limit: int = 200000

def load_crypto_env() -> Dict[str, Any]:
    return {
        "nodes": {
            "eth": NetworkSettings(os.getenv("RPC_ETH", "https://mainnet.infura.io"), 1),
            "bsc": NetworkSettings(os.getenv("RPC_BSC", "https://bsc-dataseed.binance.org"), 56)
        },
        "retry_strategy": {"attempts": 3, "delay": 1.5},
        "fee_multiplier": float(os.getenv("FEE_MUL", 1.2))
    }

class ConfigManager:
    _storage = load_crypto_env()

    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        return cls._storage.get(key, default)

    @classmethod
    def node_uri(cls, chain: str) -> str:
        net = cls._storage.get("nodes").get(chain)
        return net.rpc_url if net else ""