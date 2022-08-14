from pykrx import stock
import pandas as pd
pd.DataFrame(stock.get_index_ohlcv_by_date('2022-06-01','2022-06-30','1001'))

stock.get_market_trading_volume_by_date('2022-06-01','2022-06-30','005930')
stock.get_market_ohlcv_by_date('2022-06-01','2022-06-30','005930')