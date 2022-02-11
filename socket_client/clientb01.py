from dbms.Ddbms import LocalDBMethods2
from settings import wssmsg as wssmsgs
import websockets
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

async def listen(server:LocalDBMethods2):
    url = "ws://127.0.0.1:7890"
    async with websockets.connect(url) as ws:
        cover = wssmsgs.back_conn_init
        await ws.send(
            json.dumps(cover)
        )
        while True:
            msg = await ws.recv()
            m = json.loads(msg)
            if m['signal_type'] == 'trade':
                print(m['data'])
            elif m['signal_type'] == 'active_log':
                print(m)
            else:
                pass


def back01():
    print(f'process name {__name__}')
    print(f'parent process {os.getppid()}')
    print(f'process id {os.getpid()}')
    db = LocalDBMethods2('TDB.db')
    asyncio.get_event_loop().run_until_complete(listen(db))


if __name__ == '__main__':
    back01()





