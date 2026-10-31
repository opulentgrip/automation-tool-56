import json
import os
from typing import Any, Dict

class CryptoConfig:
    DEFAULT_SETTINGS = {
        "api_key": "",
        "base_url": "https://api.exchange.com",
        "retry_limit": 3,
        "wallet_mode": "read_only"
    }

    def __init__(self, config_path: str = "config.json"): 
        self.path = config_path
        self.settings = self._load_recursive(self.DEFAULT_SETTINGS)

    def _load_recursive(self, defaults: Dict[str, Any]) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            return defaults
        
        try:
            with open(self.path, 'r') as f:
                user_data = json.load(f)
            # Merge logic: overrides defaults with existing keys
            return {**defaults, **user_data}
        except (json.JSONDecodeError, IOError):
            return defaults

    def __getitem__(self, key: str) -> Any:
        return self.settings[key]

    def __repr__(self) -> str:
        return f"CryptoConfig({list(self.settings.keys())})"

# Usage pattern for automation-tool-56
def get_active_config() -> CryptoConfig:
    return CryptoConfig(os.getenv("APP_CONFIG_PATH", "config.json"))