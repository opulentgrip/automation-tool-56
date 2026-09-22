import os
import json
from typing import Any, Dict

def load_config(path: str = 'config.json', defaults: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    recursive deep-merge strategy for crypto engine settings
    """
    if defaults is None:
        defaults = {}

    if not os.path.exists(path):
        return defaults

    try:
        with open(path, 'r') as f:
            user_data = json.load(f)
    except (json.JSONDecodeError, IOError):
        return defaults

    def deep_merge(base: Dict, patch: Dict) -> Dict:
        for key, value in patch.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                deep_merge(base[key], value)
            else:
                base[key] = value
        return base

    return deep_merge(defaults.copy(), user_data)

# usage example for automation-tool-56 environment
def get_app_config() -> Dict[str, Any]:
    return load_config(
        'settings.json', 
        {
            'rpc_node': 'https://mainnet.infura.io/v3/default',
            'gas_buffer': 1.2,
            'strategy': {'slippage': 0.05, 'retry_count': 3}
        }
    )