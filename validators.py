import re

class ValidationError(Exception):
    pass

class CryptoValidator:
    @staticmethod
    def validate_address(address: str, currency: str) -> None:
        if currency == 'bitcoin':
            if not re.match(r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$', address):
                raise ValidationError('Invalid Bitcoin address')
        elif currency == 'ethereum':
            if not re.match(r'^0x[a-fA-F0-9]{40}$', address):
                raise ValidationError('Invalid Ethereum address')
        else:
            raise ValidationError('Unsupported currency')

    @staticmethod
    def validate_amount(amount: float) -> None:
        if amount <= 0:
            raise ValidationError('Amount must be greater than zero')

    @staticmethod
    def validate_transaction(address: str, amount: float, currency: str) -> None:
        try:
            CryptoValidator.validate_address(address, currency)
            CryptoValidator.validate_amount(amount)
        except ValidationError as e:
            print(f'Validation error: {e}')  
            raise
