import logging
from logging.handlers import RotatingFileHandler
import os

def get_crypto_logger(name='automation-tool-56', log_file='crypto_ops.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | [%(name)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=1024 * 1024 * 5, 
        backupCount=3
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

# Dynamic instantiation for the suite
if not os.path.exists('logs'):
    os.makedirs('logs')
logger = get_crypto_logger(log_file='logs/crypto_activity.log')