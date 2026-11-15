import os
import json
from typing import Any, Dict

class CryptoConfig:
    """Dynamic loader with chained fallback mechanism"""
    _DEFAULTS = {
        "rpc_url": "https://bsc-dataseed.binance.org/",
        "gas_price_gwei": 5,
        "max_slippage_pct": 0.5,
        "monitor_interval": 60
    }

    def __init__(self, path: str = "settings.json"):
        self._path = path
        self._data = self._load_file()

    def _load_file(self) -> Dict[str, Any]:
        if os.path.exists(self._path):
            try:
                with open(self._path, "r") as f:
                    return {**self._DEFAULTS, **json.load(f)}
            except (json.JSONDecodeError, IOError):
                pass
        return self._DEFAULTS.copy()

    def get(self, key: str, fallback: Any = None) -> Any:
        return self._data.get(key, fallback or self._DEFAULTS.get(key))

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"Key '{name}' not found in configuration")

    def refresh(self) -> None:
        self._data = self._load_file()

def get_config() -> CryptoConfig:
    """Singleton-ish access pattern for crypto tools"""
    if not hasattr(get_config, "_instance"):
        get_config._instance = CryptoConfig()
    return get_config._instance