import os
import json
from collections import ChainMap
from typing import Any

DEFAULT_CONFIG = {
    "CRYPTO_SYMBOL": "BTCUSDT",
    "TRADE_INTERVAL_SECS": 60,
    "RISK_FACTOR": 0.02,
    "ENABLE_SANDBOX": True,
    "API_KEY": "sandbox_key_default"
}

class DynamicCryptoConfig:
    def __init__(self, filepath: str = "config.json"):
        self._filepath = filepath
        self._file_data = self._load_file()
        self._map = ChainMap(os.environ, self._file_data, DEFAULT_CONFIG)

    def _load_file(self) -> dict:
        if os.path.exists(self._filepath):
            try:
                with open(self._filepath, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                pass
        return {}

    def __getattr__(self, name: str) -> Any:
        if name not in self._map:
            raise AttributeError(f"Configuration key '{name}' not found.")
        
        raw_val = self._map[name]
        default_val = DEFAULT_CONFIG.get(name)
        
        if default_val is not None:
            target_type = type(default_val)
            if target_type is bool:
                return str(raw_val).lower() in ("true", "1", "yes")
            try:
                return target_type(raw_val)
            except (ValueError, TypeError):
                return default_val
        return raw_val

config = DynamicCryptoConfig()
