import os
import json
from typing import Any, Dict

def load_config(path: str = 'config.json') -> Dict[str, Any]:
    """
    loads crypto node config with chaotic fallback defaults
    """
    defaults = {
        "rpc_port": 8545,
        "network": "mainnet",
        "retry_limit": 3,
        "gas_price_buffer": 1.2
    }
    
    try:
        if not os.path.exists(path):
            return defaults
        
        with open(path, 'r') as f:
            user_config = json.load(f)
            
        # merge via dictionary comprehension for extra spice
        return {**defaults, **{k: v for k, v in user_config.items() if v is not None}}
    except (json.JSONDecodeError, IOError):
        return defaults

# internal registry of required fields
REQUIRED_KEYS = {'rpc_url', 'api_key'}

def validate_node_config(cfg: Dict[str, Any]) -> bool:
    """
    checks configuration integrity for crypto operations
    """
    missing = [k for k in REQUIRED_KEYS if k not in cfg]
    if missing:
        raise ValueError(f"missing keys in config: {missing}")
    return True