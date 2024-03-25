import pyupbit

# df = pyupbit.get_ohlcv("KRW-BTC")
# print(df)


orderbook = pyupbit.get_orderbook("KRW-BTC")
bids_asks = orderbook[0]['orderbook_units']

for bid_ask in bids_asks:
    print(bid_ask)