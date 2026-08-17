import logging
from logging.handlers import RotatingFileHandler

class LogSetup:
    def __init__(self, log_file='app.log', max_bytes=10 * 1024 * 1024, backup_count=5):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def get_logger(self):
        return self.logger

if __name__ == '__main__':
    log_setup = LogSetup()
    logger = log_setup.get_logger()
    logger.info('Logger setup with rotation')
    logger.error('This is an error message')
    logger.debug('Debugging information')
