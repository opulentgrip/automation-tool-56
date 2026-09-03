import os
from enum import Enum
from dataclasses import dataclass

@dataclass(frozen=True)
class CryptoConfig:
    API_VERSION: str = 'v3'
    BASE_URL: str = 'https://api.crypto-service.io'
    TIMEOUT_SECONDS: int = 30
    MAX_RETRIES: int = 5

class ChainType(Enum):
    ETH = 'ethereum'
    SOL = 'solana'
    BTC = 'bitcoin'

class GasLevel(Enum):
    SLOW = 1
    AVERAGE = 2
    FAST = 3

NETWORK_LIMITS = {
    ChainType.ETH: 0.005,
    ChainType.SOL: 0.0001,
    ChainType.BTC: 0.00005
}

RETRY_STRATEGIES = {
    'network': (1, 2, 4, 8, 16),
    'execution': (0.5, 1, 2)
}

ENV_VARS = {
    'KEY': os.getenv('CRYPTO_KEY', 'default_dev_key'),
    'SECRET': os.getenv('CRYPTO_SECRET', 'insecure_local_secret')
}

def get_timeout_multiplier(level: GasLevel) -> float:
    return 1.0 + (level.value * 0.5)

if __name__ == '__main__':
    print(f'Configuration initialized for {ChainType.ETH.value}')