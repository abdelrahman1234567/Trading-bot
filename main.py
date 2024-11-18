import os
from binance.client import Client
from binance.enums import *
from binance import AsyncClient, BinanceSocketManager

# Set up your Binance API key and secret
api_key = 'INSERT API KEY'
api_secret = 'INSERT API SECRET'

client = Client(api_key, api_secret)

def get_current_price(symbol='DOGEUSDT'):
    try:
        ticker = client.get_ticker(symbol=symbol)
        return float(ticker['lastPrice']), ticker['closeTime']
    except Exception as e:
        print(f"Error fetching current price: {e}")
        return None, None

def get_balance(asset='DOGE'):
    try:
        balance = client.get_asset_balance(asset=asset)
        return float(balance['free'])
    except Exception as e:
        print(f"Error fetching balance: {e}")
        return 0

# Example usage
if __name__ == "__main__":
    first_usdt_balance = 397.93804431
    trading_usdt_balance = 397.93804431
    trading_doge_balance = 0
    last_price = 0.39833
    first_price = 0.39833
    
    while True:
        price, time = get_current_price()
        if price is None:
            time.sleep(60)
            continue
        
        if trading_usdt_balance > 0:
            profit = (last_price / price) * 0.99925 * 0.99925
            if profit > 1.002:
                # Uncomment after testing
                # order = place_order(side=SIDE_BUY, quantity=trading_usdt_balance) -> comment for testing
                trading_doge_balance = trading_usdt_balance / price * 0.99925 * 0.99925
                trading_usdt_balance = 0
                last_price = price
                print(f"Profit: +{profit*100-100}%")

        elif trading_doge_balance > 0:
            profit = (price / last_price) * 0.99925 * 0.99925
            if profit > 1.002:
                # Uncomment after testing
                # order = place_order(side=SIDE_SELL, quantity=trading_doge_balance) -> comment for testing
                trading_usdt_balance = price * trading_doge_balance * 0.99925 * 0.99925
                trading_doge_balance = 0
                last_price = price 
                print(f"Profit: +{profit*100-100}%")
        
        profit = -1
        potential_profit = -1
        if trading_usdt_balance > 0:
            profit = trading_usdt_balance - first_usdt_balance
            potential_profit = (last_price / price) * 0.99925 * 0.99925
        elif trading_doge_balance > 0:
            profit = trading_doge_balance * price - first_usdt_balance
            potential_profit = (price / last_price) * 0.99925 * 0.99925
        
        print(f"Current price: {price}, Last price: {last_price}, PP: {potential_profit}, Profit: {profit}$, DOGE: {trading_doge_balance}, USDT: {trading_usdt_balance}")
