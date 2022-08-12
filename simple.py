import alpaca_trade_api as tradeapi
import config

# API object used to submit orders
api = tradeapi.REST(
        key_id=config.API_KEY,
        secret_key=config.SECRET_KEY,
        base_url=config.BASE_URL
)

# Data streaming connection
conn = tradeapi.Stream(
        key_id=config.API_KEY,
        secret_key=config.SECRET_KEY,
        base_url=config.BASE_URL
)

# Subscribe to Live Order Book updates
@conn.on_quote('SPY')
async def on_quote(data):
    
    # Buying the Ask when there are more sellers
    if (
        data.ask_size > (data.bid_size * 1) 
        and float(api.get_account().cash) > data.ask_price
    ):
        o = api.submit_order(
            'SPY',1,"buy","limit","day", 
            limit_price=str(data.ask_price)
        )
        api.cancel_order(o.id)
        print('Buying at ASK', data.ask_price)
    
    # Selling to the Bid wheb there are more buyers
    if (
        data.bid_size > (data.ask_size * 1) 
        and api.list_positions()
    ):
        o = api.submit_order(
            'SPY',1,"sell","limit","day", 
            limit_price=str(data.bid_price)
        )
        api.cancel_order(o.id)
        print('Selling at BID', data.bid_price) 

# Go Live
conn.run()
