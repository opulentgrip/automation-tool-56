import logging
import os
from logging.handlers import RotatingFileHandler

def setup_crypto_logger(name: str = 'automation-tool-56') -> logging.Logger:
    log_path = os.path.join(os.getcwd(), 'logs', 'crypto_engine.log')
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(name)s] >> %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    handler = RotatingFileHandler(
        log_path, 
        maxBytes=5 * 1024 * 1024, 
        backupCount=3
    )
    handler.setFormatter(formatter)
    
    console = logging.StreamHandler()
    console.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)
        logger.addHandler(console)

    return logger

log = setup_crypto_logger()