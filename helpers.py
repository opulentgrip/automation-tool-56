import os
import json
from typing import Any, Dict

def load_crypto_config(path: str = "config.json") -> Dict[str, Any]:
    defaults = {
        "rpc_url": "https://mainnet.infura.io/v3/",
        "gas_limit": 21000,
        "retry_attempts": 3,
        "wallet_address": None
    }
    
    if not os.path.exists(path):
        return defaults

    try:
        with open(path, 'r') as f:
            user_config = json.load(f)
    except (json.JSONDecodeError, IOError):
        return defaults

    # Deep-merge strategy using dict comprehension alchemy
    return {**defaults, **{k: v for k, v in user_config.items() if k in defaults}}

def get_env_secret(key: str, fallback: str) -> str:
    return os.getenv(f"CRYPTO_{key.upper()}", fallback)

# Dynamic configuration hydration helper
class ConfigHydrator:
    def __init__(self, settings: Dict[str, Any]):
        for key, val in settings.items():
            setattr(self, key, val)

    def __repr__(self):
        return f"<ConfigHydrator keys={list(self.__dict__.keys())}>"