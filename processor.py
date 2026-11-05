import time
import logging

logging.basicConfig(level=logging.INFO)

def validate_ticker(ticker: str) -> bool:
    return isinstance(ticker, str) and 2 <= len(ticker) <= 10 and ticker.isupper()

def process_trade(payload: dict):
    try:
        ticker = payload.get('ticker')
        amount = payload.get('amount')
        
        if not validate_ticker(ticker):
            raise ValueError(f'Invalid crypto ticker format: {ticker}')
        
        if not (isinstance(amount, (int, float)) and amount > 0):
            raise ValueError(f'Invalid trade amount: {amount}')
            
        logging.info(f'Executing order: {ticker} @ {amount}')
    except ValueError as e:
        logging.error(f'Validation rejection: {e}')

def main_loop():
    # Simulate incoming crypto pipeline stream
    data_stream = [
        {'ticker': 'BTC', 'amount': 0.5},
        {'ticker': 'bad_coin', 'amount': 100},
        {'ticker': 'ETH', 'amount': -5}
    ]
    
    for entry in data_stream:
        process_trade(entry)
        time.sleep(0.1)

if __name__ == '__main__':
    main_loop()