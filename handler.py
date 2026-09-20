import sys

def validate_payload(data):
    required_keys = {'ticker', 'amount', 'side'}
    if not all(k in data for k in required_keys):
        raise ValueError(f"Missing keys: {required_keys - data.keys()}")
    if not isinstance(data['amount'], (int, float)) or data['amount'] <= 0:
        raise ValueError("Invalid amount value")
    if data['side'] not in ['buy', 'sell']:
        raise ValueError("Invalid order side")
    return True

def process_stream(data_source):
    for entry in data_source:
        try:
            if validate_payload(entry):
                print(f"Executing {entry['side']} for {entry['amount']} of {entry['ticker']}")
        except (ValueError, TypeError) as e:
            print(f"Malicious or malformed packet detected: {e}", file=sys.stderr)
            continue

if __name__ == '__main__':
    mock_packets = [
        {'ticker': 'BTC', 'amount': 0.5, 'side': 'buy'},
        {'ticker': 'ETH', 'amount': -10, 'side': 'sell'},
        {'ticker': 'SOL', 'amount': 100, 'side': 'hold'},
        {'ticker': 'DOGE', 'amount': 500, 'side': 'sell'}
    ]
    process_stream(mock_packets)