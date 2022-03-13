from settings import wssmsg as wssmsgs
from settings import sysmsg as sysmsgs
from settings import _global_ as const

from datetime import datetime, timedelta
from typing import List

import time
import requests


class UpbitNews:
    today = datetime.now()

    def __init__(self):
        # self.url = "https://api-manager.upbit.com/api/v1/notices"
        self.url = "https://api-manager.upbit.com/api/v1/notices?page=2"

    @staticmethod
    def __coin_clean(content) -> List:
        res = list()
        for _ in content:
            res = res + _.split(' : ')[1].replace(' ', '').split(',')
        return res

    @staticmethod
    def _get_coin(rows: dict) -> List:
        obj = rows['title']
        s, e = obj.index('(') + 1, obj.index(')')
        return obj[s: e].replace(' ', '').split(',')

    def _get_news(self, rptfmt: str = 'D%Y%m%dT%H:%M:%S'):
        """
        If "거래" and "추가" in article's title:
            identify it as ICO event.
        """
        r = requests.get(self.url)
        r = r.json()

        news = r['data']['list']

        # Initialize
        self.od = list()
        self.trsf = list()

        # Search Process
        for article in news:
            cond_content = "마켓 디지털 자산 추가" in article['title']

            if cond_content:
                k = self._get_coin(article)
                date = datetime.strptime(article['created_at'], '%Y-%m-%dT%H:%M:%S%z')
                today = datetime.now() - timedelta(seconds=30)
                if date.strftime(rptfmt) < today.strftime(rptfmt):
                    # continue
                    pass
                for coin in k:
                    # First Wave
                    k0 = {
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
                        "sf": 0.05
                    }

                    # Second Wave
                    k1 = {
                        "strnm": "upbit_transfer_strat",
                        "date": self.today.strftime(rptfmt),
                        "trader": None,
                        "asset_typ": "spot",
                        "symbol": coin,
                        "mir": 0.5,
                        "mim": 300,
                        "om": "limit",
                        "os": None,
                        "ot": 2,
                        "mtt": 20,
                        "sf": 0.20
                    }
                    self.od.append(k0)
                    self.trsf.append(k1)
                    print(k0)
                    print(k1)
                    self.p = k


if __name__ == "__main__":
    test = UpbitNews()
    test._get_news()
