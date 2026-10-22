import os
import json
from typing import Any, Dict

class CryptoConfig:
    """Dynamic configuration loader using attribute-based defaults."""
    _DEFAULTS = {
        "api_key": "",
        "rpc_url": "https://mainnet.infura.io/v3/",
        "trade_threshold": 0.05,
        "max_retries": 3,
        "log_level": "INFO"
    }

    def __init__(self, path: str = "config.json"):
        self._path = path
        self._data = self._load()

    def _load(self) -> Dict[str, Any]:
        if not os.path.exists(self._path):
            return self._DEFAULTS.copy()
        with open(self._path, "r") as f:
            try:
                user_config = json.load(f)
                return {**self._DEFAULTS, **user_config}
            except json.JSONDecodeError:
                return self._DEFAULTS.copy()

    def __getattr__(self, name: str) -> Any:
        return self._data.get(name, self._DEFAULTS.get(name))

    def reload(self) -> None:
        self._data = self._load()

    def __repr__(self) -> str:
        return f"CryptoConfig({self._data})"

settings = CryptoConfig()