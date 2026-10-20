import os
import json
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, path: str = 'settings.json'):
        self.path = path
        self.defaults = {
            'rpc_node': 'https://bsc-dataseed.binance.org/',
            'gas_limit': 200000,
            'retry_attempts': 3,
            'debug_mode': False
        }
        self._cache: Dict[str, Any] = {}

    def load(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            return self.defaults
        
        try:
            with open(self.path, 'r') as f:
                user_data = json.load(f)
            self._cache = {**self.defaults, **user_data}
            return self._cache
        except (json.JSONDecodeError, IOError):
            return self.defaults

    def __getattr__(self, name: str) -> Any:
        if not self._cache:
            self.load()
        return self._cache.get(name, self.defaults.get(name))

settings = ConfigLoader()

if __name__ == '__main__':
    print(f'Node: {settings.rpc_node}')