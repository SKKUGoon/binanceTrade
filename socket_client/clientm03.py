from numpy import ndarray

from settings import sysmsg as sysmsgs
from settings import wssmsg as wssmsgs

from binance import Client, ThreadedWebsocketManager
from binance.enums import ContractType, FuturesType
import ccxt
import numpy as np

from dateutil.relativedelta import FR, relativedelta
from datetime import datetime, timedelta
from collections import deque
from typing import List, Dict
import websockets
import asyncio
import json
import time


def get_token(target:str, typ:str, loc='../key.json') -> str:
    with open(loc, 'r') as file:
        dat = json.load(file)

    file.close()
    return dat[target][typ]


class BinancePremiumIndex:
    """
    Premium Index enforces price convergence between markets.
    https://www.binance.com/en/support/faq/360033525031

    <formula>
    Premium Index (P) = [Max(0, Impact Bid Price - Price Index ) - Max(0, Price Index - Impact Ask Price)] / Price Index

    <notation>
    1) Impact Bid Price
    - Impact Bid Price = The average fill price to execute the Impact Margin Notional on the Bid Price

    2) Impact Ask Price
    - Impact Ask Price = The average fill price to execute the Impact Margin Notional on the Ask Price

    3) Impact Margin Notional
    Impact Margin Notional (IMN) = 200 USDT / Initial margin rate at maximum leverage level
        - for USDT-Margined Contracts is the notional available to trade with 200 USDT worth of margin (price quote in USDT)
        - for Coin-Margined Contracts, it is the notional available to trade with 200 USD worth of margin (price quote in USD)
    (IMN is used to locate the average Impact Bid or Ask price in the order book.)

    ex) maximum leverage of the BTCUSDT : 125x. - corresponding IMN is 0.8% ( x2 of maintenance margin rate ).
        IMN = 200 USDT / 0.8% = 200 / 0.008 = 25000 USDT

        You calculate Impact Bid Price, Impact Ask Price in the order book.
    Price index can be retrieved via binance API.

    <strategy>
    If the Premium Index overshoots that is your signal.

    Delivery gets much less liquidity than the future market.
    Give liquidity to the delivery. According to the spread direction.
    Hedge your position using the perpetual future market.

    This works because people do not know about the perpetual future market and delivery market's association.
    """

    def __init__(self, target_coin:str):
        # CONSTANT
        self.ID_LIVE = get_token('binance_live', 'access_key')
        self.PW_LIVE = get_token('binance_live', 'secret_key')

        # API
        self.binancedata = Client(self.ID_LIVE, self.PW_LIVE)
        self.notion = self.calc_impact_margin_notional(target_coin)

    # SUPPORT FUNCTIONS
    def _market_leverage_info(self, ticker:str) -> Dict:
        r = self.binancedata.futures_leverage_bracket(symbol=ticker)
        return r[0]['brackets'][0]

    def calc_premium_index(self):
        # ACQUIRE DATA
        prc_idx = self.binancedata.get_margin_price_index(symbol='ETHUSDT')
        orderbook = self.binancedata.futures_order_book(symbol='ETHUSDT')

        prc_idx = float(prc_idx['price'])

        impact_bid = self.calc_impact_bid_price(orderbook['bids'], self.notion)
        impact_ask = self.calc_impact_ask_price(orderbook['asks'], self.notion)

        premium = (max(0, impact_bid - prc_idx) -
                   max(0, prc_idx - impact_ask)) / prc_idx
        return premium

    def calc_impact_margin_notional(self, ticker:str, standard:int=200):
        leverage_info = self._market_leverage_info(ticker)
        imn = leverage_info['maintMarginRatio'] * 2
        return standard / imn

    def calc_impact_bid_price(self, bid_info:[List], imn:float) -> ndarray:
        value = 0
        impact_bids = list()
        for i, j in bid_info:
            value += np.multiply(float(i), float(j))
            if value < imn:
                impact_bids.append(float(i))
            else:
                impact_bids.append(float(i))
                break

        ibp = np.mean(impact_bids)
        return ibp

    def calc_impact_ask_price(self, ask_info:[List], imn:float) -> ndarray:
        value = 0
        impact_asks = list()
        for i, j in ask_info:
            value += np.multiply(float(i), float(j))
            if value < imn:
                impact_asks.append(float(i))
            else:
                impact_asks.append(float(i))
                break
        ibp = np.mean(impact_asks)
        return ibp


if __name__ == '__main__':
    premium = BinancePremiumIndex(target_coin='ETHUSDT')
    while True:
        dt = datetime.now().strftime('%H%M%S')
        s = premium.calc_premium_index()
        print(dt, s)
        time.sleep(1)




