from dbms.Ddbms import LocalDBMethods2
import settings.table as config
import settings.sysmsg as msg

import pandas as pd
import ccxt

from typing import List
from datetime import datetime, timedelta
import json


def get_token(target:str, typ:str, loc='key.json') -> str:
    with open(loc, 'r') as file:
        dat = json.load(file)
    file.close()
    return dat[target][typ]


class NightWatch:
    invest_ratio = 0.5
    order_markup = 0.7

    def __init__(self):
        # Insert Database
        self.server = LocalDBMethods2('binance.db')
        self.server.conn.execute(
            "PRAGMA journal_mode=WAL"
        )

        # Initial State
        self.deposit = self.get_deposit()
        self.trade = False

    @property
    def __login_info(self):
        id = get_token('binance', 'access_key')
        pw = get_token('binance', 'secret_key')
        return {'apiKey': id, 'secret': pw}

    def get_deposit(self, clearing:str='USDT'):
        """
        Always have dollars as USDT.
        """
        binance = ccxt.binance(config=self.__login_info)
        blnc = binance.fetch_balance()
        return blnc[clearing]['free']

    def monitor_signal(self, threshold:int=30):
        """
        :param threshold:
            seconds base threshold.
            if threshold == 30:
                monitor signal upto 30seconds before present.
        """
        t = datetime.now()
        d = t.strftime('%Y%m%d')
        h1 = t - timedelta(seconds=threshold)

        # Monitor Signal from the database
        condition = f"date = '{d}' and time >= '{h1}'"
        cols = list(config.TABLE_EVENTDRIVEN.keys())
        r = self.server.select_db(
            target_column=cols,
            target_table=config.TABLENAME_EVENTDRIVEN,
            condition1=condition
        )
        if len(r) == 0:
            print(msg.STATUS_3)
        else:
            asset_loc = cols.index('asset')
            assets = [sig[asset_loc] for sig in r]
            print(msg.STATUS_2)
            self.trade = True

            avail = self.deposit * self.invest_ratio

            self.exec_strat(asset=assets, deposit=avail)

    def exec_strat(self, asset:List, deposit:float):
        asset_avail = deposit / len(asset)
        binance = ccxt.binance(config=self.__login_info)
        for a in asset:
            print(msg.STATUS_4)

            # Calculate Price, Amount
            p = binance.fetch_ticker(f'{a}/USDT')['close'] * self.order_markup
            am = asset_avail / p

            # Order
            order = binance.create_limit_buy_order(
                symbol=f'{a}/USDT',
                amount=am,
                price=p  # price for 1EA of coin.
            )
            print(msg.ORDERFILL.format(
                msg.ORDERFILLPADDING,
                a,
                order['info']['orderId'],
                order['amount'],
                order['price'],
                order['amount'] * order['price'],
                msg.ORDERFILLPADDING
            ))

            self.o = order


if __name__ == '__main__':
    nw = NightWatch()
