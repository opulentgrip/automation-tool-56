import os
import json
from typing import Any, Dict

def load_config(path: str = 'config.json') -> Dict[str, Any]:
    defaults = {
        'api_endpoint': 'https://api.exchange.com',
        'retry_limit': 3,
        'buffer_size': 1024,
        'strategy': 'arbitrage'
    }
    
    try:
        if os.path.exists(path):
            with open(path, 'r') as f:
                user_cfg = json.load(f)
                defaults.update(user_cfg)
    except (json.JSONDecodeError, IOError):
        pass

    class ConfigDict(dict):
        def __getattr__(self, name: str) -> Any:
            return self[name]

    return ConfigDict(defaults)

config = load_config()