import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any], path: str = 'config.json'):
        self.path = path
        self.data = defaults
        self._load_and_merge()

    def _load_and_merge(self) -> None:
        if not os.path.exists(self.path):
            return
        try:
            with open(self.path, 'r') as f:
                loaded = json.load(f)
                self.data.update({k: v for k, v in loaded.items() if k in self.data})
        except (json.JSONDecodeError, IOError):
            pass

    def __getattr__(self, name: str) -> Any:
        if name in self.data:
            return self.data[name]
        raise AttributeError(f'crypto node config missing: {name}')

def get_config() -> ConfigLoader:
    return ConfigLoader({
        'api_key': None,
        'rpc_node': 'wss://mainnet.infura.io/v3/',
        'retry_attempts': 3,
        'timeout_sec': 30,
        'wallet_addresses': []
    })