import ccxt
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime


b = ccxt.binance()
symbols = ['BTC/USDT']

dat = b.fetch_ohlcv(symbols[0], '1h')
dat = pd.DataFrame(dat, columns=['date', 'open', 'high', 'low', 'close', 'vol'])
dat.date = dat.date // 1000

dat.date = dat.date.apply(lambda x: datetime.utcfromtimestamp(x).strftime('%Y%m%d'))
dat = dat.set_index('date')

f = ccxt.binance({'options': {'defaultType': 'future'}})
m = f.load_markets()
datf = f.fetch_ohlcv(symbols[0], '1h')
datf = pd.DataFrame(datf, columns=['date', 'open', 'high', 'low', 'close', 'vol'])
datf.date = datf.date // 1000

datf.date = datf.date.apply(lambda x: datetime.utcfromtimestamp(x).strftime('%Y%m%d'))
datf = datf.set_index('date')


# ((dat.open - datf.open) / dat.open).plot(secondary_y=True)
# ((dat.open - datf.open) / dat.open).rolling(window=5).mean().plot(secondary_y=True)
# ((dat.open - datf.open) / dat.open).rolling(window=20).mean().plot(secondary_y=True)

dat.open.plot()
datf.open.plot()
plt.show()