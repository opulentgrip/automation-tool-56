import logging
from logging.handlers import RotatingFileHandler
import os

def get_crypto_logger(name='automation-tool-56'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    log_formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [wallet-daemon] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # ensure logs dir exists for the strategy state
    log_path = 'logs/trading_activity.log'
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    # custom rotation strategy: 5MB files, keep 3 versions
    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=5*1024*1024,
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setFormatter(log_formatter)

    # secondary console output for urgent crypto signals
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

# global entry point instance
crypto_logger = get_crypto_logger()