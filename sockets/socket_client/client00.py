import websockets
import asyncio
import time
import json


async def listen():
    url = "ws://127.0.0.1:7890"
    async with websockets.connect(url) as ws:
        while True:
            payload = {
                'signal_type': 'conn',
                'data': {
                    'msg': 'test_method'
                }
            }
            payload_j = json.dumps(payload)
            await ws.send(payload_j)

            msg = await ws.recv()
            m = json.loads(msg)
            print(m)
            if m['data']['status'] == 'normal':
                print(m['data']['msg'])
            else:
                raise RuntimeError
            time.sleep(5)


asyncio.get_event_loop().run_until_complete(listen())


