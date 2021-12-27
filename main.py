import settings.table as config
import settings.sysmsg as msg
from dbms.Ddbms import LocalDBMethods2
from model.N_v0 import UpBitNews

import json

import ccxt


def get_token(target:str, typ:str, loc='key.json') -> str:
    with open(loc, 'r') as file:
        dat = json.load(file)
    file.close()
    return dat[target][typ]


class SigInsert:
    def __init__(self):
        # Insert Database
        self.server = LocalDBMethods2('binance.db')
        self.server.conn.execute(
            "PRAGMA journal_mode=WAL"
        )
        self.chk_server_status()
        self.insert_signal()

    def chk_server_status(self):
        t = self.server.get_table_list()
        if "stgyedr" not in t:
            print(msg.STATUS_1, config.TABLENAME_EVENTDRIVEN)
            self.server.create_table_w_pk(
                table_name=config.TABLENAME_EVENTDRIVEN,
                variables=config.TABLE_EVENTDRIVEN,
                pk_loc=[0, 1, 2, 3, 5]
            )

        if "stgyres" not in t:
            print(msg.STATUS_1, config.TABLENAME_ACCOUNT)
            self.server.create_table_w_pk(
                table_name=config.TABLENAME_ACCOUNT,
                variables=config.TABLE_ACCOUNT,
                pk_loc=[0, 1]
            )
        print(msg.STATUS_0, "ready")

    def insert_signal(self):
        upb = UpBitNews(database=self.server)
        upb.run()


class NightWatch:
    def __init__(self):
        # Insert Database
        self.server = LocalDBMethods2('binance.db')
        ...

    @property
    def __login_info(self):
        id = get_token('binance', 'access_key')
        pw = get_token('binance', 'secret_key')
        return {'apiKey': id, 'secret': pw}

    def send_order(self):
        binance = ccxt.binance(config=self.__login_info)
        # binance.create_limit_order()


if __name__ == '__main__':
    b = SigInsert()
