import os
import json
from typing import Any, Dict

DEFAULTS: Dict[str, Any] = {
    "RPC_URL": "https://cloudflare-eth.com",
    "GAS_MULTIPLIER": 1.15,
    "SLIPPAGE_BPS": 50,
    "POLLING_INTERVAL_SEC": 12,
    "DEBUG_MODE": False,
    "ENCRYPTED_KEY_PATH": "key.enc"
}

class CryptoConfig:
    """A metamorphic config loader that dynamically resolves from environment variables,
    an optional JSON file, and hardcoded crypto defaults."""
    
    def __init__(self, filepath: str = "config.json"):
        self._filepath = filepath
        self._file_config = self._load_from_file()

    def _load_from_file(self) -> Dict[str, Any]:
        if os.path.exists(self._filepath):
            try:
                with open(self._filepath, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return {}

    def get(self, key: str) -> Any:
        default_val = DEFAULTS.get(key)
        env_val = os.getenv(key)
        
        if env_val is not None:
            if default_val is not None:
                try:
                    if isinstance(default_val, bool):
                        return env_val.lower() in ("true", "1", "yes")
                    return type(default_val)(env_val)
                except ValueError:
                    return env_val
            return env_val

        if key in self._file_config:
            return self._file_config[key]

        if key in DEFAULTS:
            return DEFAULTS[key]
        
        raise AttributeError(f"Configuration key '{key}' is undefined.")

    def __getattr__(self, name: str) -> Any:
        try:
            return self.get(name)
        except AttributeError as e:
            raise AttributeError(e) from None

config = CryptoConfig()
