from binance import ThreadedWebsocketManager, Client
from binance.enums import ContractType
import queue
import asyncio
import json

from datetime import datetime, timedelta


def get_token(target:str, typ:str, loc='key.json') -> str:
    with open(loc, 'r') as file:
        dat = json.load(file)

    file.close()
    return dat[target][typ]


class BinanceLiveStream:
    def __init__(self, ):
        self.id = get_token('binance_live', 'access_key')
        self.pw = get_token('binance_live', 'secret_key')

        self.spot_close = 'init'
        self.q_spread = queue.Queue(maxsize=20)

    def report_spot_tick(self, msg):
        best_bid = msg['b']
        best_ask = msg['a']
        print('spot', best_bid, best_ask)

    def report_swap_tick(self, msg):
        best_bid = msg['data']['b']
        best_ask = msg['data']['a']
        print('swap', best_bid, best_ask)
        pass

    def get_future_ticker(self, msg):
        client = Client(self.id, self.pw)
        symbol_info = ...

    def main(self, symbol:str):
        twm_kline = ThreadedWebsocketManager(self.id, self.pw)
        twm_tick = ThreadedWebsocketManager(self.id, self.pw)

        twm_kline.start()
        twm_tick.start()

        # TICKER
        twm_tick.start_symbol_ticker_socket(
            callback=self.report_spot_tick,
            symbol='ETHUSDT'
        )
        twm_tick.start_symbol_ticker_futures_socket(
            callback=self.report_swap_tick,
            symbol='ETHusdt_220325'
        )


        twm_kline.join()
        twm_tick.join()


if __name__ == '__main__':
    b = BinanceLiveStream()
    b.main('SANDUSDT')