import logging
from logging.handlers import RotatingFileHandler
import os

def get_crypto_logger(name='automation-tool-56', log_file='crypto_engine.log'):
    """ Initialize a rotating logger for crypto trade cycles """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Prevent duplicate handlers in interactive sessions
    if logger.hasHandlers():
        logger.handlers.clear()

    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | [%(filename)s:%(lineno)d] | %(message)s'
    )

    # Rotation at 5MB, keep 3 backup files
    handler = RotatingFileHandler(
        log_file, 
        maxBytes=5*1024*1024, 
        backupCount=3
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Stream logs to console for real-time monitoring
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

    return logger

# Instantiate standard logger for module consumption
logger = get_crypto_logger()