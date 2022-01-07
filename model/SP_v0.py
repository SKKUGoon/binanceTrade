import ccxt
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime


b = ccxt.binance()
symbols = ['ETH/USDT']

dat = b.fetch_ohlcv(symbols[0], '1m')
dat = pd.DataFrame(dat, columns=['date', 'open', 'high', 'low', 'close', 'vol'])
dat.date = dat.date // 1000

dat.date = dat.date.apply(lambda x: datetime.utcfromtimestamp(x).strftime('%Y%m%d'))
dat = dat.set_index('date')

f = ccxt.binance({'options': {'defaultType': 'future'}})
m = f.load_markets()
datf = f.fetch_ohlcv(symbols[0], '1m')
datf = pd.DataFrame(datf, columns=['date', 'open', 'high', 'low', 'close', 'vol'])
datf.date = datf.date // 1000

datf.date = datf.date.apply(lambda x: datetime.utcfromtimestamp(x).strftime('%Y%m%d'))
datf = datf.set_index('date')


# Backwardation
back = (dat.open - datf.open) / datf.open  # Positive -> Contango / Negative -> Backwardation
back.plot(secondary_y=True)
(back.rolling(window=20).mean() + (2 * back.rolling(window=20).std())).plot(secondary_y=True)
(back.rolling(window=20).mean() - (2 * back.rolling(window=20).std())).plot(secondary_y=True)

# datf.open.rolling(window=10).std().plot(secondary_y=True)
datf.open.plot()
plt.show()