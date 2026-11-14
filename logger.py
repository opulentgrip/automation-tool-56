import logging
from logging.handlers import RotatingFileHandler
import os

def get_crypto_logger(name='automation-tool-56', log_file='crypto_ops.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(process)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=5 * 1024 * 1024, 
            backupCount=3
        )
        file_handler.setFormatter(formatter)
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
    return logger

log = get_crypto_logger()

def log_trade(symbol, side, price):
    log.info(f'EXEC: {side.upper()} {symbol} at {price}')

def log_alert(msg):
    log.warning(f'ALERT: {msg}')