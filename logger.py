import logging
from logging.handlers import RotatingFileHandler
import os

def get_crypto_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not os.path.exists('logs'):
        os.makedirs('logs')
        
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'
    )

    file_handler = RotatingFileHandler(
        'logs/automation-tool-56.log',
        maxBytes=1048576 * 5,
        backupCount=3
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
    return logger

log = get_crypto_logger('crypto_bot')