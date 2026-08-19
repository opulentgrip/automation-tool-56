import logging

class CustomLogger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def debug(self, message):
        self._log_with_error_handling(self.logger.debug, message)

    def info(self, message):
        self._log_with_error_handling(self.logger.info, message)

    def warning(self, message):
        self._log_with_error_handling(self.logger.warning, message)

    def error(self, message):
        self._log_with_error_handling(self.logger.error, message)

    def critical(self, message):
        self._log_with_error_handling(self.logger.critical, message)

    def _log_with_error_handling(self, log_method, message):
        try:
            log_method(message)
        except Exception as e:
            self.logger.error(f'Logging failed: {e}')