import logging
import sys
from datetime import datetime

class CryptoFormatter(logging.Formatter):
    COLORS = {'INFO': '\033[94m', 'ERROR': '\033[91m', 'DEBUG': '\033[92m'}
    def format(self, record):
        color = self.COLORS.get(record.levelname, '\033[0m')
        return f"{color}[{datetime.now().isoformat()}] {record.levelname}: {record.getMessage()}\033[0m"

def get_crypto_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(CryptoFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
    return logger

log = get_crypto_logger('automation-tool-56')