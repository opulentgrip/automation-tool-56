import logging
import os
from logging.handlers import RotatingFileHandler

def get_crypto_logger(name='automation-tool-56', log_file='crypto_ops.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | [%(name)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Rotate at 5MB, keep 3 historical snapshots
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=5*1024*1024, 
            backupCount=3
        )
        file_handler.setFormatter(formatter)
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger

# Instantiate for global use within the tool
logger = get_crypto_logger()