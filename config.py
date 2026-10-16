import json
import os
from typing import Any, Dict

class ConfigLoader:
    """Magic configuration factory for crypto trading nodes."""
    DEFAULTS = {
        "rpc_url": "https://mainnet.infura.io/v3/",
        "gas_price_strategy": "aggressive",
        "retry_limit": 3,
        "wallet_prefix": "0x"
    }

    def __init__(self, path: str = "config.json"):
        self.path = path
        self.data = self._load()

    def _load(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            return self.DEFAULTS
        try:
            with open(self.path, "r") as f:
                user_config = json.load(f)
            return {**self.DEFAULTS, **user_config}
        except (json.JSONDecodeError, IOError):
            return self.DEFAULTS

    def get(self, key: str, fallback: Any = None) -> Any:
        return self.data.get(key, fallback)

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def __getattr__(self, item: str) -> Any:
        return self.data.get(item)

def get_config(path: str = "config.json") -> ConfigLoader:
    return ConfigLoader(path)