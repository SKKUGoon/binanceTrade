import asyncio
import json

from binance import AsyncClient, DepthCacheManager, BinanceSocketManager
from binance import ThreadedWebsocketManager


def get_token(target:str, typ:str, loc='key.json') -> str:
    with open(loc, 'r') as file:
        dat = json.load(file)
    file.close()
    return dat[target][typ]


id = get_token('binance_live', 'access_key')
pw = get_token('binance_live', 'secret_key')


def rpt_spot(msg):
    print('spot', msg)

def rpt_swap(msg):
    print('swap', msg)

def rpt_spot_t(msg):
    print('spot tickers best bid', msg['b'])
    print('spot tickers best bid', msg['a'])

def rpt_swap_t(msg):
    print('swap tickers best bid', msg['data']['b'])
    print('swap tickers best ask', msg['data']['a'])

twm = ThreadedWebsocketManager(id, pw)
twm.start()

twm.start_kline_socket(callback=rpt_spot, symbol='ETHUSDT')
twm.start_kline_futures_socket(callback=rpt_swap, symbol='ETHUSDT')

twm.start_symbol_ticker_socket(callback=rpt_spot_t, symbol='ETHUSDT')
twm.start_symbol_ticker_futures_socket(callback=rpt_swap_t, symbol='ETHUSDT')
twm.join()