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

        self.spot_close = 'init'
        self.q_spread = queue.Queue(maxsize=20)

    def report_spot(self, msg):
        """
        Report candle ticks every time the close price changes
        """
        if self.spot_close != float(msg['k']['c']):
            self.spot_close = float(msg['k']['c'])
        else:
            pass

    def report_swap(self, msg, calc:int=20):
        """
        :param msg:
        :return:
        """
        try:
            spread = (float(msg['k']['c']) - self.spot_close) / self.spot_close
            print('swap - spot', spread)
            if len(self.q_spread) == calc:

                self.q_spread.put(
                    spread
                )
            else:
                self.q_spread.put(
                    spread
                )


        except Exception as e:
            print(e)
            pass

        # print(datetime.utcfromtimestamp(msg['k']['t'] / 1000))
        # print(datetime.utcfromtimestamp(msg['k']['T'] / 1000))
        pass

    def report_spot_tick(self, msg):
        best_bid = msg['b']
        best_ask = msg['a']
        print('spot', best_bid, best_ask)

    def report_swap_tick(self, msg):
        best_bid = msg['data']['b']
        best_ask = msg['data']['a']
        print('swap', best_bid, best_ask)
        pass

    def main(self, symbol:str):
        twm_kline = ThreadedWebsocketManager(self.id, self.pw)
        twm_tick = ThreadedWebsocketManager(self.id, self.pw)

        twm_kline.start()
        twm_tick.start()

        # CANDLE LINE
        twm_kline.start_kline_socket(
            callback=self.report_spot,
            symbol=symbol
        )
        twm_kline.start_kline_futures_socket(
            callback=self.report_swap,
            symbol=symbol
        )

        # TICKER
        twm_tick.start_symbol_ticker_socket(
            callback=self.report_spot_tick,
            symbol=symbol
        )
        twm_tick.start_symbol_ticker_futures_socket(
            callback=self.report_swap_tick,
            symbol=symbol
        )

        twm_kline.join()
        twm_tick.join()



if __name__ == '__main__':
    b = BinanceLiveStream()
    b.main('ETHUSDT')