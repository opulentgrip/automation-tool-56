import os
import logging

class ConfigError(Exception):
    """Custom exception for crypto automation edge cases."""
    pass

def get_api_key():
    key = os.getenv('CRYPTO_API_KEY')
    if not key:
        raise ConfigError('API key missing from environment variables')
    return key

def validate_timeout(value):
    try:
        timeout = float(value)
        if not (0.1 <= timeout <= 60.0):
            raise ValueError
        return timeout
    except (ValueError, TypeError):
        logging.warning(f'Invalid timeout {value}, defaulting to 30.0')
        return 30.0

def load_settings():
    try:
        return {
            "key": get_api_key(),
            "timeout": validate_timeout(os.getenv('TIMEOUT', 30.0)),
            "mode": os.getenv('MODE', 'SANDBOX').upper()
        }
    except ConfigError as e:
        logging.critical(f'Startup aborted: {e}')
        return {}

SETTINGS = load_settings()