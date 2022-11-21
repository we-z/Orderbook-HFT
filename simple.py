import config
import alpaca_trade_api as tradeapi

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
    if data.bid_size > data.ask_size * 3: 
        try:
            o = api.submit_order(
                'SPY', 10, "buy", "limit", "day", 
                limit_price=str(data.ask_price)
            )
            api.cancel_order(o.id)
            print(data.timestamp,'Buying at',data.ask_price)
        except Exception as e:
            pass

    # Selling to the Bid wheb there are more buyers
    if data.ask_size > data.bid_size * 3:
        try:
            o = api.submit_order(
                'SPY', 10, "sell", "limit", "day", 
                limit_price=str(data.bid_price)
            )
            api.cancel_order(o.id)
            print(data.timestamp,'Selling at',data.bid_price) 
        except Exception as e:
            pass

# Go Live
conn.run()
