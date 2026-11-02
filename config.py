import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, path: str = 'config.json'):
        self.path = path
        self.defaults = {
            "rpc_url": "https://mainnet.infura.io/v3/",
            "retry_limit": 3,
            "gas_strategy": "aggressive"
        }

    def load(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            return self.defaults
        try:
            with open(self.path, 'r') as f:
                user_config = json.load(f)
            return {**self.defaults, **user_config}
        except (json.JSONDecodeError, IOError):
            return self.defaults

    @property
    def settings(self) -> Dict[str, Any]:
        return self.load()

config_instance = ConfigLoader()

def get_config_value(key: str, default: Any = None) -> Any:
    return config_instance.settings.get(key, default)