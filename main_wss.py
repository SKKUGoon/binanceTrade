from binance import ThreadedWebsocketManager

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

    def report_spot(self, msg):
        """
        Report candle ticks every time the close price changes
        """
        # print('spot', msg)
        pass

    def report_swap(self, msg):
        """
        :param msg:
        :return:
        """
        print('swap', 'close', msg['k']['c'])
        print(datetime.utcfromtimestamp(msg['k']['t'] / 1000))
        print(datetime.utcfromtimestamp(msg['k']['T'] / 1000))
        pass

    def report_spot_tick(self, msg):
        # print('spot tick', msg)
        pass

    def report_swap_tick(self, msg):
        # print('swap tick', msg)
        pass

    def main(self, symbol:str):
        twm = ThreadedWebsocketManager(self.id, self.pw)
        twm.start()

        # CANDLE LINE
        twm.start_kline_socket(
            callback=self.report_spot,
            symbol=symbol
        )
        twm.start_kline_futures_socket(
            callback=self.report_swap,
            symbol=symbol
        )

        # TICKER
        twm.start_symbol_ticker_socket(
            callback=self.report_spot_tick,
            symbol=symbol
        )
        twm.start_symbol_ticker_futures_socket(
            callback=self.report_swap_tick,
            symbol=symbol
        )
        twm.join()


if __name__ == '__main__':
    b = BinanceLiveStream()
    b.main('ETHUSDT')