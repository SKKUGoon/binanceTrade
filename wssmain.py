from binance import Client
from binance import ThreadedWebsocketManager, ThreadedDepthCacheManager
from binance.exceptions import BinanceAPIException

import json
import asyncio

import datetime


def get_token(target:str, typ:str, loc='key.json') -> str:
    with open(loc, 'r') as file:
        dat = json.load(file)
    file.close()
    return dat[target][typ]

id = get_token('binance_live', 'access_key')
pw = get_token('binance_live', 'secret_key')


c = Client(id, pw)
twm = ThreadedWebsocketManager()
twm.start() # Uses threads. Start() is required to be called before starting
dcm = ThreadedDepthCacheManager()

def handle_socket_message(msg):
    print(msg)

twm.start_depth_socket(
    callback=handle_socket_message,
    symbol='ETHUSDT'
)