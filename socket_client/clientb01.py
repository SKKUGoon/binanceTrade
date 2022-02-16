from dbms.Ddbms import LocalDBMethods
from settings import _global_ as const
from settings import wssmsg as wssmsgs
from settings import sysmsg as sysmsgs
from settings import table
from typing import List
import websockets
import platform
import asyncio
import time
import json
import os


# BACK OFFICE CLIENT
# NAME:
# DATABASE_INSERTION
# OBJECTIVE:
# Get Messages and Record it in Database
# FREQ: 5SECS

def db_addr():
    if platform.system() == 'Windows':
        return '../TDB.db'
    else:
        return '/home/goon/crypto/binanceTrade/TDB.db'


def insert_tlog(message:dict) -> [List]:
    """
    :param message:
    ==============================
    Trade messages
    - extract date, time, strategy_name, symbol
    :return: List of List
    """
    d, t = message['date'].replace('D', '').split('T')
    n = message['data']['strat_name']
    a = message['data']['symbol']
    return [[d, t, n, a]]


def insert_clog(message:dict):
    """
    :param message:
    ==============================
    Ping Message
    - extract date, time, module name, status
    :return: List of List
    """
    dt = message['data']['t']
    d = time.strftime("%Y%m%d", time.localtime(dt))
    t = time.strftime("%H:%M:%S", time.localtime(dt))
    n = message['data']['n']
    s = message['data']['s']
    return [[d, t, n, s]]


def delete_old(server:LocalDBMethods, modules:set) -> None:
    for n in modules:
        cond = f'module = "{n}"'
        c = server.count_rows(
            target_table=table.TABLENAME_CLIENT,
            condition=cond
        )
        if c > const.CLIENT_LOG_COUNT:
            server.delete_oldest(
                table_name=table.TABLENAME_CLIENT,
                num=1,
                condition=cond,
            )


async def listen(server:LocalDBMethods):
    # MODULES
    modules = set()

    server.set_wal()
    url = "ws://127.0.0.1:7890"
    async with websockets.connect(url) as ws:
        cover = wssmsgs.back_conn_init
        await ws.send(
            json.dumps(cover)
        )
        while True:
            msg = await ws.recv()
            m = json.loads(msg)
            if m['signal_type'] == 'spot_trade':
                server.insert_rows(
                    table_name=table.TABLENAME_STRAT,
                    col_=list(table.TABLE_STRAT.keys()),
                    rows_=insert_tlog(m)
                )
                print(sysmsgs.BACK01_DATABASE_MSG0)
            elif m['signal_type'] == 'test_trade':
                server.insert_rows(
                    table_name=table.TABLENAME_STRAT,
                    col_=list(table.TABLE_STRAT.keys()),
                    rows_=insert_tlog(m)
                )
                print(sysmsgs.BACK01_DATABASE_MSG1)
            elif m['signal_type'] == 'active_log':
                modules.add(m['data']['n'])
                server.insert_rows(
                    table_name=table.TABLENAME_CLIENT,
                    col_=list(table.TABLE_CLIENT.keys()),
                    rows_=insert_clog(m)
                )
                delete_old(server, modules=modules)
                print(sysmsgs.BACK01_DATABASE_MSG2)
            else:
                pass


def back01():
    print(f'process name {__name__}')
    print(f'parent process {os.getppid()}')
    print(f'process id {os.getpid()}')
    db = LocalDBMethods(db_addr())
    asyncio.get_event_loop().run_until_complete(listen(db))


if __name__ == '__main__':
    back01()
