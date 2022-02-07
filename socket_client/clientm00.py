from settings import wssmsg as wssmsgs
from settings import sysmsg as sysmsgs
from datetime import datetime, timedelta
from typing import List
import websockets
import asyncio
import requests
import time
import json
import os


# MIDDLE OFFICE CLIENT
# NAME:
# UPBIT_NEWS_CRAWLER
# OBJECTIVE:
# GATHER COIN ICO FROM UPBIT
# BY CONSISTANTLY PINGING IT
# FREQ: SECS

async def ping(date:str, trader:str, symbol:str, asset_typ:str, mir:float, mim:int, om:str, os:str, ot:int,
               mtt:int, sf:float, strnm:str):
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
    :return:
    """
    url = "ws://127.0.0.1:7890"

    async with websockets.connect(url) as ws:
        cover = wssmsgs.midl_conn_init
        await ws.send(
            json.dumps(cover)
        )

        payload = {
            'signal_type': 'spot_trade',
            'date': date,
            'trader': trader,
            'asset_type': asset_typ,  # spot
            'data':{
                'strat_name': strnm,
                'symbol': symbol,
                'max_invest_ratio': mir,
                'max_invest_money': mim,
                'order_method': om,  # limit, market
                'order_slice': os,
                'orderfill_time': ot,  # seconds
                'max_trade_time': mtt,
                'satisfactory': sf
            }
        }
        payload_j = json.dumps(payload)
        await ws.send(payload_j)

        msg = await ws.recv()
        print(msg)


class UpbitNews:
    today = datetime.now()
    def __init__(self):
        self.url = "https://api-manager.upbit.com/api/v1/notices"

    def __coin_clean(self, content) -> List:
        res = list()
        for _ in content:
            res = res + _.split(' : ')[1].replace(' ', '').split(',')
        return res

    def _get_coin(self, rows:dict) -> List:
        obj = rows['title']
        s, e = obj.index('(') + 1, obj.index(')')
        return obj[s : e].replace(' ', '').split(',')

    def _get_news(self, rptfmt:str='D%Y%m%dT%H:%M:%S'):
        r = requests.get(self.url)
        r = r.json()

        news = r['data']['list']

        # Initialize
        self.od = list()

        # Search Process
        for article in news:
            if ("거래" in article['title']) and ("추가" in article['title']):
                k = self._get_coin(article)
                date = datetime.strptime(article['created_at'], '%Y-%m-%dT%H:%M:%S%z')
                today = datetime.now() - timedelta(seconds=30)
                if date.strftime(rptfmt) < today.strftime(rptfmt):
                    continue
                for coin in k:
                    k = {
                        "strnm": "upbit_ico_strat",
                        "date": self.today.strftime(rptfmt),
                        "trader": None,
                        "asset_typ": 'spot',
                        "symbol": coin,
                        "mir": 0.5,
                        "mim": 300,  # Dollars
                        "om": "limit",
                        "os": None,
                        "ot": 2,
                        "mtt": 20,
                        "sf": 0.15
                    }
                    self.od.append(k)
                    print(k)
                    self.p = k

    def run(self):
        self._get_news()
        if len(self.od) == 0:
            print(
                datetime.now().strftime('%H%M%S'),
                sysmsgs.MIDDLE01_MSG_NOINFO
            )
        for orders in self.od:
            asyncio.get_event_loop().run_until_complete(
                ping(**orders)
            )
            print(
                datetime.now().strftime('%H%M%S'),
                sysmsgs.MIDDLE01_MSG_ORDER
            )
            time.sleep(60)


def middle00():
    print(f'process name {__name__}')
    print(f'parent process {os.getppid()}')
    print(f'process id {os.getpid()}')
    while True:
        try:
            ub = UpbitNews()
            while True:
                ub.run()
                time.sleep(0.25)
        except Exception as e:
            print(e)
            print(sysmsgs.MIDDLE01_MSG_ERROR)
            time.sleep(1)


if __name__ == '__main__':
    middle00()
