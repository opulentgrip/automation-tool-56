import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

class CryptoLogger:
    _instances = {}

    def __new__(cls, name='automation-tool-56'):
        if name not in cls._instances:
            instance = super().__new__(cls)
            instance._setup_logger(name)
            cls._instances[name] = instance
        return cls._instances[name]

    def _setup_logger(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | [%(name)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        file_handler = RotatingFileHandler(
            log_dir / f'{name}.log', 
            maxBytes=5*1024*1024, 
            backupCount=3
        )
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger

def get_auto_logger():
    return CryptoLogger().get_logger()