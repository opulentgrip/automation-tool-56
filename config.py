import json
import os
from typing import Any, Dict

class ConfigLoader:
    _defaults = {
        'rpc_url': 'https://mainnet.infura.io/v3/default',
        'gas_limit': 21000,
        'retry_count': 3,
        'debug': False
    }

    def __init__(self, config_path: str = 'config.json'):
        self.path = config_path
        self.data = self._load()

    def _load(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            return self._defaults
        try:
            with open(self.path, 'r') as f:
                user_config = json.load(f)
            return {**self._defaults, **user_config}
        except (json.JSONDecodeError, IOError):
            return self._defaults

    def __getattr__(self, name: str) -> Any:
        if name in self.data:
            return self.data[name]
        raise AttributeError(f'Config key {name} not found')

    def reload(self):
        self.data = self._load()

# Singleton pattern for global access
config = ConfigLoader()