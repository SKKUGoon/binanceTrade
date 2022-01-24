from dbms.Ddbms import LocalDBMethods2
from settings import wssmsg as wssmsgs
import websockets
from datetime import datetime
import asyncio
import time
import json


# BACK OFFICE CLIENT
# NAME:
# TEST_SIGNAL
# OBJECTIVE:
# CHECK WHETHER TRADING PROGRAM IS WORKING
# SIGNAL 'test_trade' MAKES THE TRADER TO CONNECT TO TEST SERVER

async def listen(rptfmt='D%Y%m%dT%H:%M:%S'):
    url = "ws://127.0.0.1:7890"
    async with websockets.connect(url) as ws:
        cover = wssmsgs.back_test_init
        date = datetime.now().strftime(rptfmt)

        await ws.send(
            json.dumps(cover)
        )

        payload = {
            'signal_type': 'test_trade',
            'date': date,
            'trader': 'binance',
            'asset_type': 'spot',
            'data':{
                'strat_name': 'test_ico_strat',
                'symbol': 'BTC',
                'max_invest_ratio': 0.1,
                'max_invest_money': 100,
                'order_method': 'limit',
                'order_slice': None,
                'orderfill_time': 2,
                'max_trade_time': 20,
                'satisfactory': 0.15
            }
        }
        await ws.send(
            json.dumps(payload)
        )
        msg = await ws.recv()
        m = json.loads(msg)
        print(m)


asyncio.get_event_loop().run_until_complete(listen())


