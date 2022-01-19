from settings import wssmsg as wssmsgs
from worker_spottrade import BinanceTrader
import websockets
import asyncio
import time
import threading
import json


# FRONT OFFICE CLIENT
# NAME:
# DATABASE_INSERTION
# OBJECTIVE:
# CHECK WHETHER BROADCASTER IS WORKING
# BY CONSISTANTLY PINGING IT
# FREQ: 5SECS

async def listen():
    btrade = BinanceTrader()
    url = "ws://127.0.0.1:7890"
    async with websockets.connect(url) as ws:
        cover = wssmsgs.frnt_conn_init
        await ws.send(
            json.dumps(cover)
        )
        while True:
            msg = await ws.recv()
            m = json.loads(msg)
            if m['signal_type'] == 'trade':
                print(m)
                t = threading.Thread(name='Binance Trader',
                                     target=btrade.process_order,
                                     kwargs=m['data'])
                t.start()
            elif m['signal_type'] == 'test_trade':
                btrade.binance.set_sandbox_mode(True)
                t = threading.Thread(target=btrade.process_order,
                                     kwargs=m['data'])
                t.start()
                btrade.binance.set_sandbox_mode(False)
            else:
                pass


asyncio.get_event_loop().run_until_complete(listen())


