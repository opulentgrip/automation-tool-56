import os
import json
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, path: str = 'settings.json'):
        self.path = path
        self.defaults = {
            "rpc_url": "https://bsc-dataseed.binance.org/",
            "gas_limit": 21000,
            "slippage": 0.005,
            "debug_mode": False
        }
        self.data = self._load()

    def _load(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            return self.defaults
        try:
            with open(self.path, 'r') as f:
                user_config = json.load(f)
                return {**self.defaults, **user_config}
        except (json.JSONDecodeError, IOError):
            return self.defaults

    def get(self, key: str, fallback: Any = None) -> Any:
        return self.data.get(key, fallback)

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    @property
    def all(self) -> Dict[str, Any]:
        return self.data

def get_config() -> ConfigLoader:
    return ConfigLoader()