import json
import os
from typing import Any, Dict

def load_crypto_config(path: str = "config.json") -> Dict[str, Any]:
    defaults = {
        "rpc_url": "https://mainnet.infura.io/v3/",
        "gas_limit": 21000,
        "retry_attempts": 3,
        "network_id": 1
    }
    
    if not os.path.exists(path):
        return defaults

    try:
        with open(path, "r") as f:
            user_config = json.load(f)
    except (json.JSONDecodeError, IOError):
        return defaults

    return {**defaults, **user_config}

def get_env_var_or_default(key: str, default: Any) -> Any:
    return os.getenv(key) if os.getenv(key) is not None else default

class ConfigProxy:
    def __init__(self, data: Dict[str, Any]):
        self._data = data
    
    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"Config key {name} not found")