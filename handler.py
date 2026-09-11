import logging

def validate_payload(data):
    required_fields = {'asset_pair', 'side', 'amount'}
    if not all(k in data for k in required_fields):
        raise ValueError(f'missing keys: {required_fields - data.keys()}')
    if not isinstance(data.get('amount'), (int, float)) or data['amount'] <= 0:
        raise ValueError('invalid amount quantity')
    return True

def run_processing_loop(event_stream):
    logger = logging.getLogger('automation-tool-56')
    for packet in event_stream:
        try:
            if validate_payload(packet):
                process_order(packet)
        except Exception as e:
            logger.error(f'input validation failure: {e}')
            continue

def process_order(data):
    # Core business logic for crypto execution
    pass

if __name__ == '__main__':
    mock_stream = [{'asset_pair': 'BTC-USDT', 'side': 'buy', 'amount': 0.5}, {'amount': -1}]
    run_processing_loop(mock_stream)