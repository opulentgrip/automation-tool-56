import logging
from logging.handlers import RotatingFileHandler
import os

def get_crypto_logger(name='automation-tool-56', log_file='crypto_engine.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] - %(message)s'
    )

    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=1024 * 1024 * 5, 
        backupCount=5
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

if __name__ == '__main__':
    # usage for crypto tracking
    log = get_crypto_logger()
    log.info('order execution module initialized')
    log.debug('api latency check: 42ms')