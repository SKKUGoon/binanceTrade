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
    def __init__(self, tick_equidistant:int=2, tick_collect:int=5):
        self.id = get_token('binance_live', 'access_key')
        self.pw = get_token('binance_live', 'secret_key')

        self.spot_close = 'init'
        self.spld, self.lpsd = deque(), deque()
        self.spld_l, self.spld_u, self.plsd_l, self.plsd_u = (
            None, None, None, None
        )
        self.equidist = tick_equidistant
        self.equimin = tick_collect

        # Tick Spread Calc Init
        self.deli_bid, self.deli_ask = None, None
        self.spread_calc = False

        # Band Calc Init
        self.time = time.time()

    def bollinger_band(self, obj:Iterable, apart:float=3.0) -> (float, float):
        m = np.mean(obj)
        s = np.std(obj)
        return (m - apart * s, m + apart * s)

    def report_perp_tick(self, msg):
        """
        Spread Calc
        [SHORT TERM] - [LONG TERM]
        (PERPETUAL)     (DELIVERY)
        ->
        PERP - DELI > 0
        PERP > DELI
        PERP SHORT, DELIVERY LONG
        (BIDDING)     (ASKING)
        """
        best_bid = float(msg['data']['b'])
        best_ask = float(msg['data']['a'])

        if self.spread_calc is True:
            # Short Perpetual Long Delivery
            spread_spld = (best_bid - self.deli_ask) / self.deli_ask
            # Long Perpetual Short Delivery
            spread_plsd = (best_ask - self.deli_bid) / self.deli_bid

            if self.spld_l is not None:
                print("perp", best_bid, best_ask)
                print("deli", self.deli_bid, self.deli_ask)
                if self.spld_l > spread_spld:
                    print('spld signal')
                    ...
            if self.plsd_l is not None:
                if self.plsd_u < spread_plsd:
                    # print('lpsd signal')
                    ...

            # Queue Process
            if len(self.spld) == 0:
                self.spld.append(spread_spld)
            if len(self.lpsd) == 0:
                self.lpsd.append(spread_plsd)

            if time.time() - self.time >= self.equidist:
                # Append spread every 2 seconds
                self.spld.append(spread_spld)
                self.lpsd.append(spread_plsd)

                # Short Perp Long Delivery
                if len(self.spld) > (60 / self.equidist) * self.equimin:
                    self.spld_l, self.spld_u = self.bollinger_band(self.spld)
                    self.spld.popleft()
                else:
                    print(
                        f"Collecting data {len(self.spld)}/{(60 / self.equidist) * self.equimin}"
                    )

                # Long Perp Short Delivery
                if len(self.lpsd) > (60 / self.equidist) * self.equimin:
                    self.plsd_l, self.plsd_u = self.bollinger_band(self.lpsd)
                    self.lpsd.popleft()
                else:
                    print(
                        f"Collecting data {len(self.lpsd)}/{(60 / self.equidist) * self.equimin}"
                    )

                self.time = time.time()

    def report_deli_tick(self, msg):
        best_bid = float(msg['data']['b'])
        best_ask = float(msg['data']['a'])

        # Globalized variable
        self.spread_calc = True
        self.deli_bid = best_bid
        self.deli_ask = best_ask

    def get_future_expr(self, dfmt='%Y%m%d'):
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

        twm_kline.join()
        twm_tick.join()


if __name__ == '__main__':
    b = BinanceLiveStream()
    b.main('ETHUSDT')