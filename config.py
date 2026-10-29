import os
import json
from typing import Any, Dict

DEFAULT_CONFIG = {
    "rpc_url": "https://mainnet.infura.io",
    "timeout": 30,
    "retry_attempts": 3,
    "gas_multiplier": 1.2
}

class ConfigManager:
    def __init__(self, path: str = "config.json"):
        self.path = path
        self.settings = self._load()

    def _load(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            return DEFAULT_CONFIG
        try:
            with open(self.path, "r") as f:
                user_data = json.load(f)
                return {**DEFAULT_CONFIG, **user_data}
        except (json.JSONDecodeError, IOError):
            return DEFAULT_CONFIG

    def get(self, key: str, fallback: Any = None) -> Any:
        return self.settings.get(key, fallback)

    def __getitem__(self, key: str) -> Any:
        return self.settings[key]

    def reload(self):
        self.settings = self._load()

config = ConfigManager()