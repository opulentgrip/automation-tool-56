import logging

class CustomLogger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(f'{name}.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_info(self, msg):
        self.logger.info(msg)

    def log_warning(self, msg):
        self.logger.warning(msg)

    def log_error(self, msg):
        self.logger.error(msg)

if __name__ == '__main__':
    logger = CustomLogger('crypto')
    logger.log_info('Starting the crypto automation tool')
    
    # Simulating some processing steps
    try:
        # This is a placeholder for a process that could fail
        data = None # Assume data is supposed to come from somewhere
        if data is None:
            raise ValueError('No data received')
        logger.log_info('Processing data')
    except ValueError as e:
        logger.log_error(f'Error: {str(e)}')
        logger.log_warning('Validation failed during processing')
    except Exception as e:
        logger.log_error(f'Unexpected error: {str(e)}')