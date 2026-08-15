class CryptoConstants:
    COINS = [
        'BTC',
        'ETH',
        'XRP',
        'LTC',
        'BCH',
    ]
    SUPPORTED_EXCHANGES = [
        'Binance',
        'Coinbase',
        'Kraken',
        'Bitfinex',
    ]
    API_KEY_ENV_VAR = 'CRYPTO_API_KEY'
    API_URL = 'https://api.crypto.com/v1/'
    DEFAULT_TIMEOUT = 30
    ERROR_MESSAGES = {
        'network_error': 'Failed to connect to the network.',
        'invalid_coin': 'The specified coin is not supported.',
        'api_error': 'Error retrieved from the API.',
    }
    @staticmethod
    def get_coin_list():
        return ', '.join(CryptoConstants.COINS)
    @staticmethod
    def get_supported_exchanges():
        return ', '.join(CryptoConstants.SUPPORTED_EXCHANGES)