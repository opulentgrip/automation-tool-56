import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name, log_file, level=logging.INFO):
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=2)
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger

# Usage example
if __name__ == '__main__':
    logger = setup_logger('crypto_logger', 'crypto.log')
    logger.info('Logger setup complete')
    logger.error('This is an error message')
    logger.warning('This is a warning message')