from settings import sysmsg as sysmsgs

from binance import ThreadedWebsocketManager
from binance.enums import ContractType
import numpy as np

from dateutil.relativedelta import FR, relativedelta
from collections import deque
from typing import Iterable
import datetime
import json
import time


def get_token(target:str, typ:str, loc='../key.json') -> str:
    with open(loc, 'r') as file:
        dat = json.load(file)

    file.close()
    return dat[target][typ]


class BinanceLiveStream:
    def __init__(self, tick_equidistant:int=2, tick_collect:int=1, abn_band:float=3.5,
                 abn_stop:float=0.5):
        # CONSTANT VARIABLE
        ## PRIVACY
        self.ID = get_token('binance_live', 'access_key')
        self.PW = get_token('binance_live', 'secret_key')

        ## BAND CALC INFO
        self.EQUIDIST = tick_equidistant
        self.EQUIMIN = tick_collect
        self.BAND_WIDTH = abn_band
        self.BAND_TARGET = abn_stop

        # MUTABLE VARIABLE
        self.spld, self.lpsd = deque(), deque()
        self.spld_l, self.spld_u, self.spld_tgt, self.spld_tgt_loc = (
            None, None, None, None
        )
        self.spld_sig = False

        ## TICK SPREAD CALC INFO
        self.deli_bid, self.deli_ask = None, None
        self.prc_deli, self.prc_perp = None, None
        self.spread_calc = False

        # TIME
        self.time = time.time()

    @staticmethod
    def bollinger_band(obj:Iterable, apart:float, ending:float) -> (float, float, float):
        m = np.mean(obj)
        s = np.std(obj)
        return m - apart * s, m + apart * s, m - ending * s

    @staticmethod
    def report_signal():
        print("")

    def qprocess_prep(self, spread_value:float) -> None:
        """
        If length of the Queue(self.spld) is 0 or below target length:
            1) add spread_value
            2) print status message
            3) Renew time clock
        ========================================
        :param spread_value:
        :return: None
        """
        self.spld.append(spread_value)
        self.time = time.time()
        print(
            sysmsgs.MIDDLE03_MSG_PREP,
            f"{len(self.spld)}/{int((60 / self.EQUIDIST) * self.EQUIMIN)}"
        )

    def _qprocess_maintain(self, spread_value:float) -> None:
        """
        If length of the Queue(self.spld) is equal to target length:
            1) popleft from the queue - O(1)
            2) append(right) the spread_value - O(1)
            3) Calculate bollinger_band - k * O(n)
        ========================================
        :param spread_value:
        :return: None
        """
        self.spld.append(spread_value)
        self.spld_l, self.spld_u, self.spld_tgt = self.bollinger_band(
            obj=self.spld,
            apart=self.BAND_WIDTH,
            ending=self.BAND_TARGET
        )
        self.spld.popleft()
        self.time = time.time()

    def qprocess_maintain_sec(self, value:float) -> None:
        if time.time() - self.time >= self.EQUIDIST:  # Append spread every {self.equidist} seconds
            print(f"SPREAD VALUE {value}")
            if len(self.spld) > (60 / self.EQUIDIST) * self.EQUIMIN:
                self._qprocess_maintain(value)
            else:
                self.qprocess_prep(value)

    def qprocess_signal_turnon(self, current_value:float) -> None:
        """
        Start if the condition is met.
            1) Turn on the spread signal.
            2) Send Ping to Broadcaster
        ========================================
        :param current_value:
        :return: None
        """
        self.spld_sig = True
        self.spld_tgt_loc = self.spld_tgt  # Object Copy

        # REPORT SIGNAL
        dt = datetime.datetime.now().strftime('%H%M%S')
        print(sysmsgs.MIDDLE03_MSG_SIG_TIME.format(dt))
        print(sysmsgs.MIDDLE03_MSG_SIG_IND_ON)
        print(sysmsgs.MIDDLE03_MSG_SIG_PRC.format(self.prc_deli, self.prc_perp))
        print(sysmsgs.MIDDLE03_MSG_SIG_SPD.format(self.deli_ask, current_value))

    def qprocess_signal_turnoff(self, current_value:float):
        """
        Start if the condition is met.
            1) Turn off the spread signal.
            2) Send Ping to Broadcaster
            3) Re-initialize the whole parameter
        ========================================
        :param current_value:
        :return:
        """
        self.spld_sig = False
        self.spld_tgt_loc = None

        # REPORT SIGNAL
        dt = datetime.datetime.now().strftime('%H%M%S')
        print(sysmsgs.MIDDLE03_MSG_SIG_TIME.format(dt))
        print(sysmsgs.MIDDLE03_MSG_SIG_IND_OFF)
        print(sysmsgs.MIDDLE03_MSG_SIG_PRC.format(self.prc_deli, self.prc_perp))
        print(sysmsgs.MIDDLE03_MSG_SIG_SPD.format(self.deli_ask, current_value))

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
        ========================================
        Every self._qprocess_[] function resets time
        ========================================
        :param msg:
        :return: None
        """
        best_bid = float(msg['data']['b'])

        if self.spread_calc is True:
            # Delivery Bid & Ask Price is In
            # Begin Calculating Spreads
            spread_spld = (self.deli_ask - best_bid)

            if self.spld_sig is False:
                if self.spld_l is not None:
                    if self.spld_l > spread_spld:
                        self.qprocess_signal_turnon(best_bid)  # After this, Signal is True

                # Queue Management
                if len(self.spld) == 0:
                    self.qprocess_prep(spread_spld)
                self.qprocess_maintain_sec(value=spread_spld)

            else:
                if self.spld_tgt_loc <= spread_spld:
                    self.qprocess_signal_turnoff(best_bid)  # After this, Signal is False

                # Queue Management
                self.qprocess_maintain_sec(value=spread_spld)

    def report_deli_tick(self, msg):
        best_bid = float(msg['data']['b'])
        best_ask = float(msg['data']['a'])

        # Globalized variable
        self.deli_bid = best_bid
        self.deli_ask = best_ask
        self.spread_calc = True

    def report_deli_kline(self, msg):
        self.prc_deli = float(msg['k']['c'])

    def report_perp_kline(self, msg):
        self.prc_perp = float(msg['k']['c'])

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

    def main(self, symbol:str):
        twm_kline = ThreadedWebsocketManager(self.ID, self.PW)
        twm_tick = ThreadedWebsocketManager(self.ID, self.PW)

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
            callback=self.report_perp_kline,
            symbol=f'{symbol}'
        )
        twm_kline.start_kline_futures_socket(
            callback=self.report_deli_kline,
            symbol=symbol,
            contract_type=ContractType.CURRENT_QUARTER
        )

        twm_kline.join()
        twm_tick.join()


if __name__ == '__main__':
    b = BinanceLiveStream()
    b.main('ETHUSDT')
