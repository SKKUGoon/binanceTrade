from datetime import datetime
from typing import List
import time
import requests


class UpBitNews:
    def __init__(self, test:bool=False):
        self.url = "https://api-manager.upbit.com/api/v1/notices"
        self.run(test=test)

    def __coin_clean(self, content) -> List:
        res = list()
        for _ in content:
            res = res + _.split(' : ')[1].replace(' ', '').split(',')
        return res

    def _get_article(self, news_id:int) -> (str, str):
        news = requests.get(f"{self.url}/{news_id}")
        news = news.json()

        body = news['data']['body']
        body = body.split('.')
        i = 0
        for i in range(len(body)):
            if "추가됩니다" in body[i]:
                break

        result = [
            _ for _ in (map(lambda x: x.replace('\r', ''),
                            body[i + 1].split('\n')))
            if (len(_) > 0) and ('마켓') in _
        ]
        krw_coin = [notice for notice in result
                    if 'krw'.upper() in notice]
        btc_coin = [notice for notice in result
                    if 'btc'.upper() in notice]
        return (self.__coin_clean(krw_coin) +
                self.__coin_clean(btc_coin))

    def _get_news(self):
        r = requests.get(self.url)
        r = r.json()

        try:
            news = r['data']['list']
            db_row = list()
            for article in news:
                if "거래" in article['title']:
                    if "추가" in article['title']:
                        k = self._get_article(article['id'])
                        date = datetime.strptime(article['created_at'],
                                                 '%Y-%m-%dT%H:%M:%S%z')
                        for coin in k:
                            row_ = (
                                date.strftime('%Y%m%d'),
                                date.strftime('%H%M%S'),
                                coin,
                                "ico_event",
                                'long'
                            )
                            print(row_)

        except Exception as e:
            print(e)

    def run(self, test:bool=False):
        if test is True:
            print("Test")
            for i in range(1):
                self._get_news()
                time.sleep(5)

        else:
            while True:
                self._get_news()
                time.sleep(5)


if __name__ == '__main__':
    upb = UpBitNews()
