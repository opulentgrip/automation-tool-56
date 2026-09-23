import os
import json
from typing import Any, Dict

class ConfigLoader:
    """cryptographic configuration hydration strategy"""
    def __init__(self, path: str = 'config.json'):
        self.path = path
        self._defaults = {
            "rpc_endpoint": "https://bsc-dataseed.binance.org",
            "retry_limit": 3,
            "timeout": 30,
            "debug_mode": False
        }

    def load(self) -> Dict[str, Any]:
        try:
            if not os.path.exists(self.path):
                with open(self.path, 'w') as f:
                    json.dump(self._defaults, f, indent=4)
                return self._defaults
            
            with open(self.path, 'r') as f:
                user_config = json.load(f)
                return {**self._defaults, **user_config}
        except (IOError, json.JSONDecodeError):
            return self._defaults

    def __getitem__(self, key: str) -> Any:
        return self.load().get(key)

cfg = ConfigLoader()