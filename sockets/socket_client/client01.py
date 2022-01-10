import websockets
import asyncio
import time
import json


async def listen():
    url = "ws://127.0.0.1:7890"

    async with websockets.connect(url) as ws:
        payload = {
            'signal_type': 'trade',
            'data':{
                'strat_name': 'upbit_ico_strat',
                'symbol': 'ETH/USDT',
                'max_invest_ratio': 0.1,
                'max_invest_money': 100000,
                'order_method': 'limit',  # limit, market
                'orderfill_time': 2,  # seconds
                'max_trade_time': 20,
                'satisfactory': 0.15
            }
        }
        payload_j = json.dumps(payload)
        await ws.send(payload_j)

        msg = await ws.recv()
        print(msg)


asyncio.get_event_loop().run_until_complete(listen())
