import threading

import numpy as np
import ccxt

from typing import Dict, List
import json
import time
import math
import os


def get_token(target:str, typ:str, loc='..\key.json') -> str:
    with open(loc, 'r') as file:
        dat = json.load(file)
    file.close()
    return dat[target][typ]


class BinanceFuture:
    """
    Trades Binance Future with open delta
    """
    def __init__(self):
        print("[BinanceFuture] StandBy")
        self.binance = ccxt.binance(config=self.login_config)
        self.marketinfo = self.binance.load_markets()

    def set_market_leverage(self, symbol:str, leverage:int=20):
        if "/" in symbol:
            symbol = symbol.replace("/", "")
        print(f"[BinanceSpread] Seeting {symbol} leverage to {leverage}")
        self.binance.fapiPrivate_post_leverage({
            'symbol': symbol,
            'leverage': leverage
        })

    def login_check(self):
        self.binance = ccxt.binance(config=self.login_config)
        self.marketinfo = self.binance.load_markets()
        self.balance = self.get_balance()

    @property
    def login_config(self) -> Dict:
        id = get_token('binance', 'access_key')
        pw = get_token('binance', 'secret_key')
        c = {
            'apiKey': id,
            'secret': pw,
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

    def _get_trading_info(self, symbol:str, using:float) -> (float, float):
        rounddown = self.marketinfo[symbol]['precision']
        amount_pre = rounddown['amount']
        amt = self.decimal_rounddown(using, amount_pre)
        return amt

    def enter_position(self, **kwargs):
        ...

    def check_position(self):
        ...

    def close_position(self):
        ...

    def process_order(self, **kwargs):
        ...
