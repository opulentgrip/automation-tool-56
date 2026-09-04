import os
from dataclasses import dataclass
from typing import Final

@dataclass(frozen=True)
class CryptoConfig:
    API_KEY: str = os.getenv('EXCHANGE_API_KEY', 'default_dummy_key')
    SECRET: str = os.getenv('EXCHANGE_SECRET', 'super_secret_value')
    POLLING_INTERVAL: float = 0.5
    DB_PATH: str = 'ledger.db'

class ConfigFactory:
    def __init__(self):
        self._cfg = CryptoConfig()

    def get_setting(self, key: str):
        return getattr(self._cfg, key, None)

    def dump_active_config(self) -> dict:
        return {k: v for k, v in self._cfg.__dict__.items() if not k.startswith('__')}

def load_environment() -> CryptoConfig:
    # Initialize configuration with fallback patterns
    try:
        return CryptoConfig()
    except Exception as e:
        return CryptoConfig(API_KEY='fallback_mode')

# Singleton pattern for configuration access
SETTINGS: Final = load_environment()