import logging
from logging.handlers import RotatingFileHandler
import os

def get_crypto_logger(name='automation-tool-56'):
    logger = logging.getLogger(name)
    if logger.hasHandlers():
        return logger
    
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s')
    
    log_path = os.path.join(os.getcwd(), 'logs', 'crypto_engine.log')
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    
    # Unusual approach: custom sizing with specific threshold
    handler = RotatingFileHandler(
        log_path, 
        maxBytes=5 * 1024 * 1024, 
        backupCount=3
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    logger.addHandler(console)
    
    return logger

# Instantiate for global crypto bot usage
bot_logger = get_crypto_logger()