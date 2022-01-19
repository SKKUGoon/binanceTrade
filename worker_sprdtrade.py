import threading

import ccxt

import json
import time
import math
import os


def get_token(target:str, typ:str, loc='.\key.json') -> str:
    p = os.path.abspath('key.json')
    with open(loc, 'r') as file:
        dat = json.load(file)
    file.close()
    return dat[target][typ]


class BinanceSpread:
    def __init__(self):
        print("[BinanceSpread] StandBy")
        self.binance = ccxt.binance(config=self.login_config)
        self.marketinfo = self.binance.load_markets()
        self.balance = self.get_balance()

    def login_check(self):
        self.binance = ccxt.binance(config=self.login_config)
        self.marketinfo = self.binance.load_markets()
        self.balance = self.get_balance()

    @property
    def login_config(self):
        id = get_token('binance', 'access_key')
        pw = get_token('binance', 'secret_key')
        c = {
            'apiKey': id,
            'secret':pw,
            'options':
                {
                    'defaultType': 'future'
                }
        }
        return c

    def get_balance(self, clearing:str='USDT'):
        b = self.binance.fetch_balance()
        return b[clearing]['free']

    @staticmethod
    def decimal_rounddown(value:float, decimal:int) -> float:
        p = int(math.floor(value * (10 ** decimal)))
        p = p / (10 ** decimal)
        return float(f'%.{decimal}f'%(p))

    def _get_trading_vol(self, mir:float, mim:int):
        return min(self.balance * mir, mim)

    def _get_trading_info(self, symbol:str, using:float) -> (float, float):
        # All Trades are going to be market price based
        rounddown = self.marketinfo[symbol]['precision']
        amount_pre = rounddown['amount']
        amt = self.decimal_rounddown(1, amount_pre)
        return amt

    # TODO: MAKE JSON FILES


if __name__ == '__main__':
    bs = BinanceSpread()