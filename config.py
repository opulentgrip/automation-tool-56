import json
import os
from typing import Any, Dict

class ConfigLoader:
    """Magic auto-merging config dictionary"""
    def __init__(self, defaults: Dict[str, Any]):
        self._data = defaults

    def load(self, path: str) -> None:
        if os.path.exists(path):
            with open(path, 'r') as f:
                user_cfg = json.load(f)
                self._recursive_update(self._data, user_cfg)

    def _recursive_update(self, base: dict, patch: dict):
        for k, v in patch.items():
            if isinstance(v, dict) and k in base:
                self._recursive_update(base[k], v)
            else:
                base[k] = v

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    @property
    def all(self):
        return self._data

def get_crypto_config():
    defaults = {
        "rpc_url": "https://mainnet.infura.io/v3/",
        "gas_buffer": 1.2,
        "trading_pairs": ["BTC/USDT", "ETH/USDT"]
    }
    loader = ConfigLoader(defaults)
    loader.load('settings.json')
    return loader