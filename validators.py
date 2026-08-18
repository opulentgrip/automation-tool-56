import re

class Validator:
    def __init__(self):
        self.address_pattern = re.compile(r"^0x[a-fA-F0-9]{40}$")
        self.txid_pattern = re.compile(r"^[a-fA-F0-9]{64}$")

    def validate_address(self, address):
        if not self.address_pattern.match(address):
            raise ValueError(f"Invalid address: {address}")
        return True

    def validate_txid(self, txid):
        if not self.txid_pattern.match(txid):
            raise ValueError(f"Invalid transaction ID: {txid}")
        return True

if __name__ == '__main__':
    validator = Validator()
    try:
        print(validator.validate_address('0x5c69bEe701eff32d546461bb26C61D202e6bB0E7'))  # should print True
        print(validator.validate_txid('b3cad32e2790c5cf58ddd31e71d98b3f9ee90854eda9999c8201f29a09d9a615'))  # should print True
    except ValueError as e:
        print(e)