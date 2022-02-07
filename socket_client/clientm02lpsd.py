from settings import sysmsg as sysmsgs
from settings import wssmsg as wssmsgs

from binance import ThreadedWebsocketManager
from binance.enums import ContractType
import numpy as np

from dateutil.relativedelta import FR, relativedelta
from collections import deque
from typing import Iterable
import websockets
import datetime
import asyncio
import json
import time
import os


async def ping(date:str, trader:str, signal:bool, symbol_l:str, symbol_s:str, asset_typ:str, mir:float, mim:int, om:str, os:str, ot:int,
               mtt:int, sf:float, lc:float, strnm:str):
    """
    :param date: ping date
    :param trader: trading platform in {'binance'}
    :param symbol: ticker name of the asset
    :param mir: maximum investable ratio in float
    :param mim: maximum investable money in integer
    :param om: order method in {'limit', 'market'}
    :param os: order slicing in {'twap', 'vwap', None}
    :param ot: orderfill waiting time(seconds) in integer
    :param mtt: maximum trading time(seconds) in integer
    :param sf: satisfactory return to drawdown.
    :param strnm: strategy name
    :param lc: loss cut
    :return:
    """
    url = "ws://127.0.0.1:7890"

    async with websockets.connect(url) as ws:
        cover = wssmsgs.midl_conn_init
        await ws.send(
            json.dumps(cover)
        )

        payload = {
            'signal_type': 'spread_trade',
            'date': date,
            'trader': trader,
            'asset_type': asset_typ,  # spot
            'data':{
                'strat_name': strnm,
                'long_or_short': signal,
                'symbol_long': symbol_l,
                'symbol_short': symbol_s,
                'max_invest_ratio': mir,
                'max_invest_money': mim,
                'order_method': om,  # limit, market
                'order_slice': os,
                'orderfill_time': ot,  # seconds
                'max_trade_time': mtt,
                'satisfactory': sf,
                'loss_cut': lc,
            }
        }
        payload_j = json.dumps(payload)
        await ws.send(payload_j)

        msg = await ws.recv()
        print(msg)


def get_token(target:str, typ:str, loc='../key.json') -> str:
    with open(loc, 'r') as file:
        dat = json.load(file)

    file.close()
    return dat[target][typ]


class BinanceLiveStream:
    def __init__(self, tick_equidistant:int=30, tick_collect:int=5, abn_band:float=5.5,
                 abn_stop:float=-0.5):
        # CONSTANT VARIABLE
        ## PRIVACY
        self.ID = get_token('binance_live', 'access_key')
        self.PW = get_token('binance_live', 'secret_key')

        ## BAND CALC INFO
        self.EQUIDIST = tick_equidistant
        self.EQUIMIN = tick_collect
        self.BAND_WIDTH = abn_band
        self.BAND_TARGET = abn_stop

        ## PING
        self.loop1 = asyncio.get_event_loop()
        self.loop2 = asyncio.get_event_loop()

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
