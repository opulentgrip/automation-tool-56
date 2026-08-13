class CryptoDataError(Exception):
    """Base class for exceptions in this module."""
    pass

class DataFormatError(CryptoDataError):
    """Exception raised for errors in the data format."""
    def __init__(self, message='Data format is invalid.', *args):
        self.message = message
        super().__init__(self.message, *args)

class NetworkError(CryptoDataError):
    """Exception raised for network-related errors."""
    def __init__(self, message='Network issue encountered.', *args):
        self.message = message
        super().__init__(self.message, *args)

class DataNotFoundError(CryptoDataError):
    """Exception raised when data cannot be found."""
    def __init__(self, message='Requested data not found.', *args):
        self.message = message
        super().__init__(self.message, *args)

class RateLimitExceededError(CryptoDataError):
    """Exception raised when API rate limit is exceeded."""
    def __init__(self, message='API rate limit exceeded.', *args):
        self.message = message
        super().__init__(self.message, *args)