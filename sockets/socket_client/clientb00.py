from settings import wssmsg as wssmsgs
import websockets
import asyncio
import time
import json


# BACK OFFICE CLIENT
# NAME:
# CONNECTION_CHECKER
# OBJECTIVE:
# CHECK WHETHER BROADCASTER IS WORKING
# BY CONSISTANTLY PINGING IT
# FREQ: 5SECS

async def listen():
    url = "ws://127.0.0.1:7890"
    async with websockets.connect(url) as ws:
        cover = wssmsgs.back_conn_init
        await ws.send(
            json.dumps(cover)
        )
        while True:
            # PING
            payload = {
                'signal_type': 'conn',
                'data': {
                    'msg': 'test_method'
                }
            }
            payload_j = json.dumps(payload)
            await ws.send(payload_j)

            # PONG
            msg = await ws.recv()
            m = json.loads(msg)
            if m['signal_type'] == 'conn_resp':
                if m['data']['status'] == 'normal':
                    print(m['data']['msg'])
            else:
                pass
            time.sleep(5)


asyncio.get_event_loop().run_until_complete(listen())


