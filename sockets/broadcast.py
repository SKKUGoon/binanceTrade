from settings import wssmsg as wssmsgs
from settings import sysmsg as sysmsgs

import websockets
import asyncio
import json

PORT = 7890

print(f"Server listening on port: {PORT}")

backoffice = set()
middleoffice = set()
frontoffice = set()

async def echo(websocket, path):
    print(sysmsgs.BROADCAST_TOTL_SIG0)
    try:
        async for message in websocket:
            print(f"[WS] {message}")
            m = json.loads(message)

            if m['signal_type'] == 'init':
                department = m['data']['dep']
                if department == 'back':
                    print("[WS] BackOffice has +1 Client")
                    backoffice.add(websocket)
                elif department == 'midl':
                    print("[WS] MiddleOffice has +1 Client")
                    middleoffice.add(websocket)
                else:
                    print("[WS] FrontOffice has +1 Client")
                    frontoffice.add(websocket)

            # CONNECTION TEST SIGNALS
            elif m['signal_type'] == 'conn':
                print(sysmsgs.BROADCAST_BACK_SIG0)
                payload = json.dumps(wssmsgs.back_conn_resp)
                for backs in backoffice:
                    await backs.send(payload)

            # TRADE SIGNALS
            elif m['signal_type'] == 'trade':
                print(sysmsgs.BROADCAST_MIDD_SIG0)
                payload = json.dumps(wssmsgs.midl_trde_resp)
                await websocket.send(payload)

                for back in backoffice:
                    await back.send(message)

                for middle in middleoffice:
                    await middle.send(payload)

                for front in frontoffice:
                    await front.send(message)

            else:
                await websocket.send("m")

    except Exception as e:
        print(e)
        print(sysmsgs.BROADCAST_TOTL_SIG1)

    finally:
        # connected.remove(websocket)
        ...


start_server = websockets.serve(echo, "localhost", PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()