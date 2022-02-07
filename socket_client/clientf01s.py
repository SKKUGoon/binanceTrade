from settings import wssmsg as wssmsgs
from worker_sprdtrade import BinanceSpread
import websockets
import asyncio
import time
import threading
import json
import os


# FRONT OFFICE CLIENT
# NAME:
# SPREAD TRADER
# OBJECTIVE:
# IF 'SPREAD_TRADE' SIGNAL IS RECEIVED
# TRADE SPREAD USING BinanceSpread API

async def listen():
    spread_trade = BinanceSpread(
        short_symbol="ETH/USDT",
        long_symbol="ETHUSDT_220325",
    )
    url = "ws://127.0.0.1:7890"
    async with websockets.connect(url) as ws:
        cover = wssmsgs.frnt_conn_init
        await ws.send(
            json.dumps(cover)
        )
        while True:
            msg = await ws.recv()
            m = json.loads(msg)
            if m['signal_type'] == 'spread_trade':
                if m['data']['long_or_short'] is True:
                    # Signal On
                    t = threading.Thread(target=spread_trade.enter_spread_short_buy,
                                         kwargs=m['data'])
                else:
                    # Signal Off
                    t = threading.Thread(target=spread_trade.exit_spread_short_sell,
                                         kwargs=m['data'])
                t.start()
                print(m['data'])

            else:
                pass


def front01s():
    print(f'process name {__name__}')
    print(f'parent process {os.getppid()}')
    print(f'process id {os.getpid()}')
    asyncio.get_event_loop().run_until_complete(listen())


if __name__ == "__main__":
    front01s()


