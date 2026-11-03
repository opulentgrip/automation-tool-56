import json
import os
from pathlib import Path
from typing import Any, Dict

class ConfigLoader:
    DEFAULT_SETTINGS = {
        "rpc_url": "https://mainnet.infura.io/v3/",
        "retry_limit": 3,
        "wallet_path": "./wallets",
        "fee_multiplier": 1.2
    }

    def __init__(self, config_path: str = "config.json"):
        self.path = Path(config_path)
        self._config = self._load()

    def _load(self) -> Dict[str, Any]:
        if not self.path.exists():
            with open(self.path, "w") as f:
                json.dump(self.DEFAULT_SETTINGS, f, indent=4)
            return self.DEFAULT_SETTINGS
        
        with open(self.path, "r") as f:
            data = json.load(f)
            return {**self.DEFAULT_SETTINGS, **data}

    def get(self, key: str, fallback: Any = None) -> Any:
        return self._config.get(key, fallback)

    def __getattr__(self, name: str) -> Any:
        if name in self._config:
            return self._config[name]
        raise AttributeError(f"config key '{name}' missing")