from dbms.Ddbms import LocalDBMethods2
import settings.table as config
import settings.sysmsg as msg

import pandas as pd
import ccxt

from typing import List, Dict
from datetime import datetime, timedelta
import threading
import json
import time


def get_token(target:str, typ:str, loc='key.json') -> str:
    with open(loc, 'r') as file:
        dat = json.load(file)
    file.close()
    return dat[target][typ]


class NightWatch:
    # Before Trade
    invest_ratio = 0.8
    order_markup = 0.7

    # Trade Parameters
    orderfill_time = 5  # seconds
    max_trade_time = 60  # seconds
    satisfy = 0.2  # satisfying return


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
    def __login_info(self) -> Dict:
        id = get_token('binance', 'access_key')
        pw = get_token('binance', 'secret_key')
        return {'apiKey': id, 'secret': pw}

    def get_deposit(self, clearing:str='USDT') -> float:
        """
        Always have dollars as USDT.
        """
        binance = ccxt.binance(config=self.__login_info)
        blnc = binance.fetch_balance()
        return blnc[clearing]['free']

    def monitor_signal(self, threshold:int=30) -> None:
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

        # TEST
        r = [('20211222', '130001', 'GTC', 'ico_event', 'long', 'upbit'),
             ('20211222', '130001', 'OCEAN', 'ico_event', 'long', 'upbit')]

        if len(r) == 0:
            print(msg.STATUS_3)
        else:
            asset_loc = cols.index('asset')
            assets = [sig[asset_loc] for sig in r]
            print(msg.STATUS_2)

            # Start Running Binance
            self.binance = ccxt.binance(config=self.__login_info)
            self.trade = True
            avail = self.deposit * self.invest_ratio

            for a in assets:
                t = threading.Thread(
                    target=self.exec_strat,
                    args=(a, avail)
                )
                t.start()

    @staticmethod
    def __alert_order(order, asset:str):
        print(msg.ORDERFILL.format(
            msg.ORDERFILLPADDING,
            asset,
            order['info']['orderId'],
            order['amount'],
            order['price'],
            order['amount'] * order['price'],
            msg.ORDERFILLPADDING
        ))

    @staticmethod
    def __alert_cancel(order, asset:str):
        print(msg.ORDERCANCEL.format(
            msg.ORDERFILLPADDING,
            asset,
            order['info']['orderId'],
            msg.ORDERFILLPADDING
        ))

    def exec_strat(self, asset:str, deposit:float) -> None:
        ####################################################################
        # Trade Thread Start
        tn = threading.currentThread().getName()
        asset_avail = deposit / len(asset)
        print(msg.STATUS_4.format(asset, tn))

        ####################################################################
        # Calculate Price, Amount
        p = self.binance.fetch_ticker(f'{asset}/USDT')['close'] * self.order_markup
        am = asset_avail / p

        ####################################################################
        # Buy Order(LIMIT)
        ts = time.time()
        print('trying', am, p)
        order = self.binance.create_limit_buy_order(
            symbol=f'{asset}/USDT',
            amount=am,
            price=p  # price for 1EA of coin.
        )
        self.__alert_order(order, asset)

        ####################################################################
        # Check Orderfilled
        ts_orderfill = time.time()
        fill = 0
        cost = None
        while (time.time() - ts_orderfill) < self.orderfill_time:
            print(f"{round(time.time() - ts_orderfill, 2)}sec passed'")
            orderinfo = self.binance.fetch_order(
                id=order['id'],
                symbol=f"{asset}/USDT"
            )
            if orderinfo['filled'] > 0:
                fill = 1  # Partial Fill
                cost = orderinfo['price']

            if orderinfo['filled'] >= 1:
                fill = 2  # Full Order Fill
                cost = orderinfo['price']

            time.sleep(0.5)

        ####################################################################
        # Orderfill Aftermath
        if fill == 0:
            print(msg.STATUS_5)
            cancel = self.binance.cancel_order(
                id=order['id'],
                symbol=f"{asset}/USDT"
            )
            self.__alert_cancel(cancel, asset)
            return
        elif fill == 1:
            print(msg.STATUS_6)
            cancel = self.binance.cancel_order(
                id=order['id'],
                symbol=f"{asset}/USDT"
            )
            self.__alert_cancel(cancel, asset)
        else:
            print(msg.STATUS_7)

        ####################################################################
        # Amount to Sell
        ams = self.binance.fetch_balance()['asset']
        assert cost is not None, "Manual Override"

        ####################################################################
        # Check Condition FullFill
        while True:
            te = time.time()

            # Condition 1: Time Limit of 60 seconds
            if (ts - te) >= self.max_trade_time:
                print(msg.EXIT_0)
                break

            # Condition 2: Return Achieved
            prc = self.binance.fetch_ticker(f'{asset}/USDT')
            if (prc - cost) / cost > self.satisfy:
                print(msg.EXIT_1)
                break

        ####################################################################
        # Sell(MARKET)
        order = self.binance.create_market_sell_order(
            symbol=f'{asset}/USDT',
            amount=ams
        )
        self.__alert_order(order, asset)
        return


if __name__ == '__main__':
    nw = NightWatch()
    nw.monitor_signal()
