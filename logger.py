import logging
import os
from logging.handlers import RotatingFileHandler

def get_crypto_logger(name='automation-tool-56'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not os.path.exists('logs'):
        os.makedirs('logs')

    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [wallet-guard] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    rotating_handler = RotatingFileHandler(
        'logs/crypto_activity.log',
        maxBytes=1024 * 1024 * 5,
        backupCount=3
    )
    rotating_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(rotating_handler)
    logger.addHandler(console_handler)
    
    return logger

log = get_crypto_logger()