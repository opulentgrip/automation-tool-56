import sys
import time
from datetime import datetime

class CryptoLogger:
    def __init__(self, prefix: str = 'AUTO56'):
        self.prefix = prefix
        self.colors = {'INFO': '\033[94m', 'WARN': '\033[93m', 'ERROR': '\033[91m', 'END': '\033[0m'}

    def _format(self, level: str, msg: str) -> str:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return f"{self.colors.get(level, '')}[{timestamp}] [{self.prefix}] [{level}] {msg}{self.colors['END']}"

    def info(self, message: str):
        sys.stdout.write(self._format('INFO', message) + '\n')

    def warn(self, message: str):
        sys.stdout.write(self._format('WARN', message) + '\n')

    def error(self, message: str):
        sys.stderr.write(self._format('ERROR', message) + '\n')

    def trace(self, data: dict):
        for key, val in data.items():
            self.info(f"  >> {key:<12} : {val}")

def get_logger(name: str = 'automation-tool-56'):
    return CryptoLogger(name)