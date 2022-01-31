from binance import ThreadedWebsocketManager
from binance.enums import ContractType
from dateutil.relativedelta import FR, relativedelta
import datetime
from collections import deque
import json
import time
from typing import Iterable
import numpy as np


def get_token(target:str, typ:str, loc='key.json') -> str:
    with open(loc, 'r') as file:
        dat = json.load(file)

    file.close()
    return dat[target][typ]


class BinanceLiveStream:
    def __init__(self, tick_equidistant:int=2, tick_collect:int=1):
        self.id = get_token('binance_live', 'access_key')
        self.pw = get_token('binance_live', 'secret_key')

        self.spot_close = 'init'
        self.spld, self.lpsd = deque(), deque()
        self.spld_l, self.spld_u, self.lpsd_l, self.lpsd_u = (
            None, None, None, None
        )
        self.equidist = tick_equidistant
        self.equimin = tick_collect

        # Tick Spread Calc Init
        self.deli_bid, self.deli_ask = None, None
        self.prc_deli, self.prc_perp = None, None
        self.spread_calc = False

        # Band Calc Init
        self.time = time.time()

    @staticmethod
    def bollinger_band(obj:Iterable, apart:float=3.5) -> (float, float):
        m = np.mean(obj)
        s = np.std(obj)
        return m - apart * s, m + apart * s

    def report_perp_tick(self, msg):
        """
        Spread Calc
        [SHORT TERM] - [LONG TERM]
        (PERPETUAL)     (DELIVERY)
        ->
        PERP - DELI > 0
        PERP > DELI
        PERP SHORT, DELIVERY LONG ( SPLD )
        (BIDDING)     (ASKING)
        """
        best_bid = float(msg['data']['b'])

        if self.spread_calc is True:
            # Short Perpetual Long Delivery
            spread_spld = (best_bid - self.deli_ask) / self.deli_ask

            print(self.prc_deli, self.prc_perp)
            if self.spld_l is not None:
                # print("perp", best_bid, best_ask)
                # print("deli", self.deli_bid, self.deli_ask)
                if self.spld_l > spread_spld:
                    print('spld signal', 'price deli', self.prc_deli, 'price perp', self.prc_perp, 'DELI 매수1호가', self.deli_ask, 'PERP 매도1호가', best_bid)

            # Queue Process
            if len(self.spld) == 0:
                self.spld.append(spread_spld)

            if time.time() - self.time >= self.equidist:
                # Append spread every 2 seconds
                self.spld.append(spread_spld)

                # Short Perp Long Delivery
                if len(self.spld) > (60 / self.equidist) * self.equimin:
                    self.spld_l, self.spld_u = self.bollinger_band(self.spld)
                    self.spld.popleft()
                else:
                    print(
                        f"Collecting data {len(self.spld)}/{(60 / self.equidist) * self.equimin}"
                    )
                self.time = time.time()

    def report_deli_tick(self, msg):
        best_bid = float(msg['data']['b'])
        best_ask = float(msg['data']['a'])

        # Globalized variable
        self.spread_calc = True
        self.deli_bid = best_bid
        self.deli_ask = best_ask

    @staticmethod
    def get_future_expr(dfmt='%Y%m%d'):
        """
        Binance Future always expires on
        LAST FRIDAY OF THE MONTH.
        """
        expr_month = {
            1: 2, 2: 1, 3: 0,
            4: 2, 5: 1, 6: 0,
            7: 2, 8: 1, 9: 0,
            10: 2, 11: 1, 12: 0
        }
        m = datetime.date.today().month
        last_fri = (
                datetime.date.today() +
                relativedelta(day=31, weekday=FR(-1), months=expr_month[m])
        )
        return f"_{last_fri.strftime(dfmt)[2:]}"

    def get_deli_kline(self, msg):
        self.prc_deli = float(msg['k']['c'])

    def get_perp_kline(self, msg):
        self.prc_perp = float(msg['k']['c'])

    def main(self, symbol:str):
        twm_kline = ThreadedWebsocketManager(self.id, self.pw)
        twm_tick = ThreadedWebsocketManager(self.id, self.pw)

        twm_kline.start()
        twm_tick.start()

        # ORDER BOOK
        expr_month = self.get_future_expr()
        twm_tick.start_symbol_ticker_futures_socket(
            callback=self.report_perp_tick,
            symbol=symbol
        )  # PERPETUAL
        twm_tick.start_symbol_ticker_futures_socket(
            callback=self.report_deli_tick,
            symbol=f'{symbol}{expr_month}'
        )  # CURRENT QUARTERS

        # Price Checker
        twm_kline.start_kline_futures_socket(
            callback=self.get_perp_kline,
            symbol=f'{symbol}'
        )
        twm_kline.start_kline_futures_socket(
            callback=self.get_deli_kline,
            symbol=symbol,
            contract_type=ContractType.CURRENT_QUARTER
        )
        print(f'{symbol}{expr_month}')

        twm_kline.join()
        twm_tick.join()


if __name__ == '__main__':
    b = BinanceLiveStream()
    b.main('ETHUSDT')