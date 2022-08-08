import alpaca_trade_api as tradeapi
import config
import time

opts = {}
opts['key_id'] = config.API_KEY
opts['secret_key'] = config.SECRET_KEY
opts['base_url'] = config.BASE_URL

# API object used to submit orders
api = tradeapi.REST(**opts)
# Data streaming connection
conn = tradeapi.Stream(**opts)

t = True
symbol = 'AAPL'
@conn.on_quote(symbol)
async def on_quote(data):
    global t
    if t:
        if data.bid_size > (data.ask_size * 4):
            api.submit_order(symbol, 100, "buy", 
                                "market", "day")
            print('Buy at BID', data.bid_price,
                        'ASK', data.ask_price)
            t = False
        if data.ask_size > (data.bid_size * 4):
            api.submit_order(symbol, 100, "sell", 
                                "market", "day")
            print('Sell at BID', data.bid_price,
                        'ASK', data.ask_price)
            t = False
    if data.ask_size == data.bid_size and not t:
        api.close_all_positions()
        print('Close at BID', data.bid_price, 
                        'ASK', data.ask_price)
        time.sleep(1)
        t = True

conn.run()
