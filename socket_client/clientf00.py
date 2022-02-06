from settings import wssmsg as wssmsgs
from worker_spottrade import BinanceTrader
import websockets
import asyncio
import time
import threading
import json


# FRONT OFFICE CLIENT
# NAME:
# SPOT TRADER
# OBJECTIVE:
# IF 'SPOT_TRADE' SIGNAL IS RECEIVED
# TRADE SPOT TRADE USING BinanceTrader API

async def listen():
    spot_trade = BinanceTrader()
    url = "ws://127.0.0.1:7890"
    async with websockets.connect(url) as ws:
        cover = wssmsgs.frnt_conn_init
        await ws.send(
            json.dumps(cover)
        )
        while True:
            msg = await ws.recv()
            m = json.loads(msg)
            if m['signal_type'] == 'spot_trade':
                print(m)
                t = threading.Thread(name='Binance Trader',
                                     target=spot_trade.process_order,
                                     kwargs=m['data'])
                t.start()
            elif m['signal_type'] == 'test_trade':
                spot_trade.binance.set_sandbox_mode(True)
                t = threading.Thread(target=spot_trade.process_order,
                                     kwargs=m['data'])
                t.start()
                spot_trade.binance.set_sandbox_mode(False)
            else:
                pass


def front00():
    asyncio.get_event_loop().run_until_complete(listen())


if __name__ == "__main__":
    front00()


