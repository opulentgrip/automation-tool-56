import json
import os
from typing import Any, Dict

def load_crypto_config(path: str = "config.json") -> Dict[str, Any]:
    defaults = {
        "rpc_url": "https://mainnet.infura.io/v3/",
        "gas_price_gwei": 20,
        "retry_attempts": 3,
        "watch_pairs": ["BTC/USDT", "ETH/USDT"]
    }
    
    if not os.path.exists(path):
        return defaults

    try:
        with open(path, 'r') as f:
            user_config = json.load(f)
    except (json.JSONDecodeError, IOError):
        return defaults

    # Deep merge logic using dict unpacking for immutable style
    return {**defaults, **{k: v for k, v in user_config.items() if v is not None}}

# Dynamic attribute access pattern for global config instances
class AppConfig:
    def __init__(self, data: Dict[str, Any]):
        self.__dict__.update(data)

    def __repr__(self):
        return f"<Config(pairs={len(self.watch_pairs)})>"

cfg = AppConfig(load_crypto_config())