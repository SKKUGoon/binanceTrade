import threading

import ccxt

import json
import time
import math


def get_token(target:str, typ:str, loc='../key.json') -> str:
    with open(loc, 'r') as file:
        dat = json.load(file)
    file.close()
    return dat[target][typ]


class BinanceTrader:
    def __init__(self):
        print("[BinanceTrader] StandBy")
        self.binance = ccxt.binance(config=self.login_config)
        self.balance = self.get_balance()
        self.marketinfo = self.binance.load_markets()

        self.ORDERMARKUP = 0.05

    def login_check(self):
        self.binance = ccxt.binance(config=self.login_config)
        self.balance = self.get_balance()
        self.marketinfo = self.binance.load_markets()

    @property
    def login_config(self):
        id = get_token('binance', 'access_key')
        pw = get_token('binance', 'secret_key')
        return {'apiKey': id, 'secret': pw}

    def get_balance(self, clearing:str='USDT'):
        b = self.binance.fetch_balance()
        return b[clearing]['free']

    @staticmethod
    def decimal_rounddown(value:float, decimal:int) -> float:
        p = int(math.floor(value * (10 ** decimal)))
        p = p / (10 ** decimal)
        return float(f'%.{decimal}f'%(p))

    def _get_trading_vol(self, mir:float, mim:int) -> float:
        return min(self.balance * mir, mim)

    def _get_trading_info(self, symbol, using:float) -> (float, float):

        rounddown = self.marketinfo[f'{symbol}/USDT']['precision']
        price_pre, amount_pre = rounddown['price'], rounddown['amount']
        prc = self.decimal_rounddown(
            self.binance.fetch_ticker(f'{symbol}/USDT')['close'] * (1 + self.ORDERMARKUP),
            price_pre
        )
        amt = self.decimal_rounddown(using / prc, amount_pre)
        return prc, amt

    def _get_order_check(self, symbol:str, orderid, orderamount):
        orderinfo = self.binance.fetch_order(
            id=orderid,
            symbol=f"{symbol}/USDT"
        )
        if orderinfo['remaining'] >= orderamount:
            fill = 0  # Trade Unsuccessful
            cost = None
        elif orderinfo['remaining'] > 0:
            fill = 1  # Partial Fill
            cost = orderinfo['price']
        else:
            fill = 2  # Full Order Fill
            cost = orderinfo['price']
        return fill, cost

    def _get_order_clean(self, state:int, orderid, symbol:str):
        if (state == 0) or (state == 1):
            try:
                cancel = self.binance.cancel_order(
                    id=orderid,
                    symbol=f"{symbol}/USDT"
                )
            except Exception as e:
                print(e)

    def _get_pre_sell(self, symbol):
        volume = self.get_balance(clearing=symbol)
        rounddown = self.marketinfo[f'{symbol}/USDT']['precision']
        amount_pre = rounddown['amount']
        volume = self.decimal_rounddown(volume, amount_pre)
        return volume

    def _get_exit_window(self, time_start, mtt:int, symbol:str, cost:float, sf:float):
        while True:
            te = time.time()
            print(te - time_start, 'sec')

            if (te - time_start) >= mtt:
                return

            prc = self.binance.fetch_ticker(f'{symbol}/USDT')['close']
            if ((prc - cost) / cost) > sf:
                return
            time.sleep(0.25)

    def process_order(self, strat_name:str, symbol:str, max_invest_ratio:float,
                      max_invest_money:int, order_method:str, order_slice:str,
                      orderfill_time:int, max_trade_time:int, satisfactory:float):
        if f"{symbol}/USDT" not in self.marketinfo.keys():
            print("[BinanceTrader] Coin not traded in Binance")
            return

        print(f"[BinanceTrader] Execute {strat_name} for {symbol} on {threading.currentThread().getName()}")

        money_invest = self._get_trading_vol(
            mir=max_invest_ratio,
            mim=max_invest_money
        )
        p, v = self._get_trading_info(
            symbol=symbol,
            using=money_invest
        )

        if order_method == 'limit':
            log_start_time = time.time()
            ################### BUY ###################
            order = self.binance.create_limit_buy_order(
                symbol=f"{symbol}/USDT",
                amount=v,
                price=p
            )
            ################### WAIT ###################
            time.sleep(orderfill_time)
            # CHECK ORDERFILLED
            order_result, order_cost = self._get_order_check(
                symbol=symbol,
                orderid=order['id'],
                orderamount=v
            )
            ############# CLEANUP ORDER ################
            self._get_order_clean(
                symbol=symbol,
                orderid=order['id'],
                state = order_result,
            )
            ################ SELL PREP #################
            vs = self._get_pre_sell(symbol=symbol)
            self._get_exit_window(
                symbol=symbol,
                time_start=log_start_time,
                cost=order_cost,
                mtt=max_trade_time,
                sf=satisfactory
            )
            ################### SELL ###################
            order = self.binance.create_market_sell_order(
                symbol=f'{symbol}/USDT',
                amount=vs
            )
            return

        elif order_method == 'market':
            order = self.binance.create_market_buy_order(
                symbol=f"{symbol}/USDT",
                amount=v
            )



if __name__ == '__main__':
    bt = BinanceTrader()

