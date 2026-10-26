import logging
from logging.handlers import RotatingFileHandler
import os

def get_crypto_logger(name='automation-tool-56', log_file='crypto_trade.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(module)s:%(lineno)d | %(message)s'
    )
    
    # Rotate at 5MB, keep 3 historical logs
    handler = RotatingFileHandler(
        log_file, 
        maxBytes=5*1024*1024, 
        backupCount=3
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    # Also stream to console for immediate trade monitoring
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)
    
    return logger

# Instantiate singleton logger for the bot
log = get_crypto_logger()