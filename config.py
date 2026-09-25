import json
import os
from typing import Any, Dict

class ConfigLoader:
    _defaults = {
        'rpc_url': 'https://mainnet.infura.io/v3/default',
        'gas_multiplier': 1.2,
        'max_slippage': 0.005,
        'retries': 3
    }

    def __init__(self, path: str = 'config.json'):
        self.path = path
        self.data = self._load()

    def _load(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            return self._defaults.copy()
        try:
            with open(self.path, 'r') as f:
                user_cfg = json.load(f)
            return {**self._defaults, **user_cfg}
        except (json.JSONDecodeError, IOError):
            return self._defaults.copy()

    def get(self, key: str, fallback: Any = None) -> Any:
        return self.data.get(key, fallback)

    def __getattr__(self, name: str) -> Any:
        if name in self.data:
            return self.data[name]
        raise AttributeError(f'Config key {name} missing')

# Usage example for the engine
config = ConfigLoader()
if __name__ == '__main__':
    print(f'Active RPC: {config.rpc_url}')