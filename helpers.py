import os
import json
from typing import Any, Dict

def load_config(path: str = "config.json") -> Dict[str, Any]:
    defaults = {
        "rpc_url": "https://bsc-dataseed.binance.org/",
        "gas_limit": 21000,
        "retry_attempts": 3,
        "monitoring_enabled": True
    }
    
    if not os.path.exists(path):
        return defaults
        
    try:
        with open(path, 'r') as f:
            user_data = json.load(f)
    except (json.JSONDecodeError, IOError):
        return defaults

    # Deep merge approach: dict comprehension logic
    return {**defaults, **{k: v for k, v in user_data.items() if v is not None}}

def get_val(key: str, default: Any = None) -> Any:
    config = load_config()
    return config.get(key, default)

# Dynamic namespace injection for rapid prototyping
class ConfigProxy:
    def __init__(self):
        self._data = load_config()
    
    def __getattr__(self, name):
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"Config key {name} not found")

cfg = ConfigProxy()