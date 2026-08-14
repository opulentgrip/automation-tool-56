import json
import re

def is_valid_crypto_address(address: str, network: str) -> bool:
    patterns = {
        'bitcoin': r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$',
        'ethereum': r'^0x[a-fA-F0-9]{40}$',
        'litecoin': r'^[LM3][a-zA-Z0-9]{26,33}$'
    }
    pattern = patterns.get(network)
    if not pattern:
        raise ValueError(f'Unsupported network: {network}')  
    return bool(re.match(pattern, address))

def parse_crypto_data(data: str) -> dict:
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        raise ValueError('Invalid JSON data')

# Example usage
if __name__ == '__main__':
    print(is_valid_crypto_address('1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa', 'bitcoin'))
    print(parse_crypto_data('{"key": "value"}'))