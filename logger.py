import sys
import logging
from datetime import datetime

class CryptoFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[94m',
        'INFO': '\033[92m',
        'WARNING': '\033[93m',
        'ERROR': '\033[91m',
        'CRITICAL': '\033[41m'
    }
    RESET = '\033[0m'

    def format(self, record):
        log_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        color = self.COLORS.get(record.levelname, self.RESET)
        msg = super().format(record)
        return f'{color}[{log_time}] {record.levelname:8}{self.RESET} | {msg}'

def get_crypto_logger(name: str = 'automation-tool-56'):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(CryptoFormatter('%(message)s'))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

stream = get_crypto_logger()