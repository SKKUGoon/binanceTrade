from settings import wssmsg as wssmsgs
from settings import sysmsg as sysmsgs
from datetime import datetime, timedelta
from typing import List
from html.parser import HTMLParser
import websockets
import asyncio
import requests
import time
import json


# MIDDLE OFFICE CLIENT
# NAME:
# BITHUMB_NEWS_CRAWLER
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
            'signal_type': 'trade',
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


class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self._open = False
        self._bag = list()
        self._bag_of_bag = list()

    def handle_starttag(self, tag, attrs) -> None:
        if tag == 'tr':
            self._open = True

    def handle_endtag(self, tag) -> None:
        if tag == 'tr':
            self._open = False
            self._bag.append(self._bag_of_bag)

            # Re - Initialize()
            self._bag_of_bag = list()

    def handle_data(self, data) -> None:
        if self._open is True:
            self._bag_of_bag.append(data.replace(' ', ''))


class BitThumbNews:
    today = datetime.now()

    def __init__(self, holding:int=140):
        self.url = "https://cafe.bithumb.com/view/boards/43"
        self.header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        self.holdings = holding

    @staticmethod
    def is_english(val:str) -> bool:
        try:
            val.encode(encoding='utf-8').decode('ascii')
        except UnicodeDecodeError:
            return False
        else:
            return True

    def _get_news(self) -> str:
        prm = {'noticeCategory': 9, 'pageNumber': 0}

        r = requests.get(
            self.url,
            headers=self.header,
            params=prm
        )
        res = r.content.decode('utf-8')
        r.close()
        return res

    def get_news(self, dfmt:str='%H:%M') -> None:
        c = self._get_news()
        parser = MyHTMLParser()
        parser.feed(c)
        num, title, date = 1, 4, 7

        self.bitthumb_news = list()
        for r in parser._bag[1:]:
            cond1 = r[title][:8] == "[상장/이벤트]"
            cond2 = r[title][:4] == "[상장]"
            if cond1 or cond2:
                if ':' in r[date]:
                    # Information for today
                    cur = (datetime.now() - timedelta(minutes=2)).strftime(dfmt)
                    if cur > r[date]:
                        # Past Information (more than 2 minutes old)
                        continue

                    # Current Information
                    if "마켓" in r[title]:  # '마켓상장', '마켓추가'
                        msg = r[title][8:]

                        # Detect coin ticker without regex
                        coin_ls = list(
                            map(
                                lambda x: x.split(')')[0],
                                msg.split('(')[1:]
                            )
                        )

                        # Get only the ticker code
                        for i in coin_ls:
                            if not self.is_english(i):
                                coin_ls.remove(i)

                        self.bitthumb_news.extend(coin_ls)

    def mkorder(self, coin:str, rptfmt:str='D%Y%m%dT%H:%M:%S'):
        k = {
            "strnm": "bitthumb_ico_strat",
            "date": self.today.strftime(rptfmt),
            "trader": None,
            "asset_typ": 'spot',
            "symbol": coin,
            "mir": 0.2,
            "mim": 100,  # Dollars
            "om": "limit",
            "os": None,
            "ot": 2,
            "mtt": 20,
            "sf": 0.15
        }
        return k

    def run(self):
        self.get_news()
        coins = list(map(self.mkorder, self.bitthumb_news))
        ordersend = False  # Default State
        if len(coins) == 0:
            print(
                datetime.now().strftime('%H%M%S'),
                sysmsgs.MIDDLE02_MSG_NOINFO
            )
        else:
            ordersend = True
            for order in coins:
                asyncio.get_event_loop().run_until_complete(
                    ping(**order)
                )
        if ordersend is True:
            print(
                datetime.now().strftime('%H%M%S'),
                sysmsgs.MIDDLE02_MSG_ORDER
            )
            time.sleep(self.holdings)


if __name__ == '__main__':
    bn = BitThumbNews()
    while True:
        bn.run()
        time.sleep(0.25)
