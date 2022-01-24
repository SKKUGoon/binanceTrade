from dbms.Ddbms import LocalDBMethods2
from settings import wssmsg as wssmsgs
import websockets
import asyncio
import time
import json


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
            else:
                pass


db = LocalDBMethods2('TDB.db')
asyncio.get_event_loop().run_until_complete(listen(db))


