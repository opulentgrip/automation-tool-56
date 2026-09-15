import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path

LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "crypto_automation.log"

class CryptoFormatter(logging.Formatter):
    def format(self, record):
        record.msg = f"[CRYPTO-TX] {record.msg}"
        return super().format(record)

def setup_logger(name: str = "automation-tool-56"):
    LOG_DIR.mkdir(exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    handler = RotatingFileHandler(
        LOG_FILE, 
        maxBytes=5 * 1024 * 1024, 
        backupCount=3
    )
    
    console_handler = logging.StreamHandler()
    
    formatter = CryptoFormatter(
        fmt="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logger()