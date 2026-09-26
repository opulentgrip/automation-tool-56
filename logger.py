import logging
import sys
from datetime import datetime

class CryptoFormatter(logging.Formatter):
    COLORS = {'DEBUG': '\033[94m', 'INFO': '\033[92m', 'WARNING': '\033[93m', 'ERROR': '\033[91m'}
    def format(self, record):
        color = self.COLORS.get(record.levelname, '\033[0m')
        timestamp = datetime.now().strftime('%H:%M:%S')
        return f"{color}[{timestamp}] {record.levelname}: {record.getMessage()}\033[0m"

def get_crypto_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(CryptoFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
    return logger

def log_trade_event(logger: logging.Logger, pair: str, amount: float, price: float):
    logger.info(f"EXECUTION: {pair} | QTY: {amount:.4f} @ ${price:.2f}")

def log_anomaly(logger: logging.Logger, signal: str):
    logger.error(f"ANOMALY DETECTED: {signal.upper()} - IMMEDIATE ATTENTION REQUIRED")