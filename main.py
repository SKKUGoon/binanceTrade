from dbms.Ddbms import LocalDBMethods2
import json

import ccxt


def get_token(target:str, typ:str, loc='key.json') -> str:
    with open(loc, 'r') as file:
        dat = json.load(file)
    file.close()
    return dat[target][typ]


class BinanceTrade:
    def __init__(self):
        info = self.__login_info
        self.binance = ccxt.binance(config=info)
        ...

    @property
    def __login_info(self):
        id = get_token('binance', 'access_key')
        pw = get_token('binance', 'secret_key')
        return {'apiKey': id, 'secret': pw}

    def get_balance(self):
        bal = self.binance.fetch_balance()
        for i in bal['info']['balances']:
            print(i)

    def send_order(self):
        self.binance.create_limit_order()


if __name__ == '__main__':
    b = BinanceTrade()