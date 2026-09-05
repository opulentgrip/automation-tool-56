import json
import os
from collections import ChainMap
from pathlib import Path
from typing import Any, Dict


class ConfigLoader:
    """Dynamic hierarchical configuration loader for crypto automation."""

    DEFAULT_CONFIG: Dict[str, Any] = {
        "network": "ethereum_mainnet",
        "rpc_url": "https://eth.llamarpc.com",
        "max_gas_gwei": 50.0,
        "slippage_percent": 0.5,
        "retry_attempts": 3,
        "enable_flashbots": False,
        "monitored_pairs": ["ETH/USDC", "WBTC/ETH"],
    }

    def __init__(self, filepath: str = "config.json", env_prefix: str = "CRYPTO_"):
        self._path = Path(filepath)
        self._prefix = env_prefix
        self._store = self._build_cascade()

    def _get_env_overrides(self) -> Dict[str, Any]:
        overrides = {}
        for key, default_val in self.DEFAULT_CONFIG.items():
            env_key = f"{self._prefix}{key.upper()}"
            if env_key in os.environ:
                raw = os.environ[env_key]
                target_type = type(default_val)
                if target_type is bool:
                    overrides[key] = raw.lower() in ("1", "true", "yes")
                elif target_type is list:
                    overrides[key] = [x.strip() for x in raw.split(",") if x.strip()]
                else:
                    overrides[key] = target_type(raw)
        return overrides

    def _load_file(self) -> Dict[str, Any]:
        if self._path.exists():
            try:
                with open(self._path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                pass
        return {}

    def _build_cascade(self) -> ChainMap:
        return ChainMap(
            self._get_env_overrides(),
            self._load_file(),
            self.DEFAULT_CONFIG.copy(),
        )

    def __getattr__(self, name: str) -> Any:
        if name in self._store:
            return self._store[name]
        raise AttributeError(f"Configuration key '{name}' not found")

    def __getitem__(self, item: str) -> Any:
        return self._store[item]

    def as_dict(self) -> Dict[str, Any]:
        return dict(self._store)
