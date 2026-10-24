import os
import json
from typing import Any, Dict

class CryptoConfig:
    def __init__(self, path: str = 'config.json'):
        self.path = path
        self._defaults = {
            "rpc_url": "https://bsc-dataseed.binance.org/",
            "retry_limit": 3,
            "gas_strategy": "aggressive",
            "monitoring_enabled": True
        }
        self.data = self._load()

    def _load(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            return self._defaults
        try:
            with open(self.path, 'r') as f:
                loaded = json.load(f)
                return {**self._defaults, **loaded}
        except (json.JSONDecodeError, IOError):
            return self._defaults

    def __getattr__(self, name: str) -> Any:
        return self.data.get(name)

    def __repr__(self) -> str:
        return f"<CryptoConfig settings={list(self.data.keys())}>"

def get_config() -> CryptoConfig:
    return CryptoConfig()