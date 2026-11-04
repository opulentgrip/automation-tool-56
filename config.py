import json
import os
from typing import Any, Dict

class CryptoConfig:
    def __init__(self, file_path: str = "config.json"):
        self.path = file_path
        self.defaults = {
            "api_key": "",
            "secret": "",
            "leverage": 5,
            "base_asset": "BTC",
            "rpc_url": "https://mainnet.infura.io/v3/"
        }
        self.data = self._load_and_merge()

    def _load_and_merge(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            return self.defaults
        
        try:
            with open(self.path, "r") as f:
                user_config = json.load(f)
        except (json.JSONDecodeError, IOError):
            return self.defaults

        return {**self.defaults, **user_config}

    def __getattr__(self, name: str) -> Any:
        return self.data.get(name, self.defaults.get(name))

    def __repr__(self) -> str:
        return f"CryptoConfig(keys={list(self.data.keys())})"

cfg = CryptoConfig()