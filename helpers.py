import json
import os
from typing import Any, Dict

def load_crypto_config(path: str = 'config.json') -> Dict[str, Any]:
    defaults = {
        'rpc_node': 'https://mainnet.infura.io/v3/default',
        'gas_limit': 21000,
        'max_retries': 3,
        'monitor_interval': 60
    }
    
    try:
        if os.path.exists(path):
            with open(path, 'r') as f:
                user_config = json.load(f)
            defaults.update({k: v for k, v in user_config.items() if v is not None})
    except (json.JSONDecodeError, IOError):
        pass
        
    return defaults

class ConfigProxy:
    def __init__(self, data: Dict[str, Any]):
        self.__dict__.update(data)

    def __getattr__(self, item: str) -> Any:
        return None

config = ConfigProxy(load_crypto_config())