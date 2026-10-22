import os
import json
from typing import Any, Dict

class ConfigLoader:
    _defaults = {
        'rpc_url': 'https://mainnet.infura.io/v3/default',
        'gas_limit': 21000,
        'retry_attempts': 3,
        'debug_mode': False
    }

    def __init__(self, path: str = 'settings.json'):
        self.path = path
        self.data = self._load()

    def _load(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            return self._defaults
        try:
            with open(self.path, 'r') as f:
                user_cfg = json.load(f)
            return {**self._defaults, **user_cfg}
        except (json.JSONDecodeError, IOError):
            return self._defaults

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def __getattr__(self, name: str) -> Any:
        if name in self.data:
            return self.data[name]
        raise AttributeError(f'Config key {name} not found')

config = ConfigLoader()