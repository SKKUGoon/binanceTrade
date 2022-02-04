from settings import sysmsg as sysmsgs
from settings import wssmsg as wssmsgs

from binance import Client, ThreadedWebsocketManager
from binance.enums import ContractType, FuturesType
import numpy as np

from dateutil.relativedelta import FR, relativedelta
from collections import deque
from typing import Iterable
import websockets
import datetime
import asyncio
import json
import time

def get_token(target:str, typ:str, loc='./key.json') -> str:
    with open(loc, 'r') as file:
        dat = json.load(file)

    file.close()
    return dat[target][typ]


class BinanceTakerVolume:
    def __init__(self, tick_equidistant:int=2, tick_collect:int=5, abn_band:float=4.5,
                 abn_stop:float=0.0):
        # CONSTANT VARIABLE
        ## PRIVACY
        self.ID = get_token('binance_live', 'access_key')
        self.PW = get_token('binance_live', 'secret_key')

        self.c = Client(self.ID, self.PW)

    @staticmethod
    def get_future_expr(dfmt='%Y%m%d') -> str:
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

    def rpt(self, msg):
        if msg['data']['m']:
            print(msg['data'])

    def main(self, symbol='ETHUSDT'):
        twm_tick = ThreadedWebsocketManager(self.ID, self.PW)

        twm_tick.start()

        # ORDER BOOK
        expr_month = self.get_future_expr()
        self.long_symbol, self.short_symbol = f'{symbol}{expr_month}', symbol
        twm_tick.start_aggtrade_futures_socket(
            callback=self.rpt,
            symbol=symbol
        )
        twm_tick.join()


if __name__ == '__main__':
    btv = BinanceTakerVolume()
