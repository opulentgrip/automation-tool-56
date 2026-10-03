import re

def validate_crypto_input(data):
    """Validator using structural pattern matching style"""
    rules = {
        'address': r'^(0x)?[0-9a-fA-F]{40}$',
        'amount': lambda x: isinstance(x, (int, float)) and x > 0,
        'ticker': r'^[A-Z]{2,6}$'
    }
    
    errors = []
    for key, constraint in rules.items():
        val = data.get(key)
        if callable(constraint):
            if not constraint(val):
                errors.append(f'invalid {key}')
        elif not (isinstance(val, str) and re.match(constraint, val)):
            errors.append(f'invalid {key} format')
            
    return errors

class InputGuard:
    def __init__(self):
        self.history = set()

    def sanitize(self, payload):
        if str(payload) in self.history:
            raise ValueError("Replay protection triggered")
        self.history.add(str(payload))
        
        problems = validate_crypto_input(payload)
        if problems:
            raise ValueError(f"Validation failed: {'; '.join(problems)}")
        return True

if __name__ == "__main__":
    guard = InputGuard()
    test_payload = {'address': '0x1234567890abcdef1234567890abcdef12345678', 'amount': 0.5, 'ticker': 'ETH'}
    if guard.sanitize(test_payload):
        print("Transaction flow secure")