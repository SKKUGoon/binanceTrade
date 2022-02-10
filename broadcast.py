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
discordoffice = set()


async def echo(websocket):
    print(sysmsgs.BROADCAST_TOTL_SIG0)
    try:
        async for message in websocket:
            m = json.loads(message)

            if m['signal_type'] == 'init':
                department = m['data']['dep']
                if department == 'back':
                    print(sysmsgs.BROADCAST_BACK_SIG0)
                    backoffice.add(websocket)
                elif department == 'midl':
                    print(sysmsgs.BROADCAST_MIDD_SIG0)
                    middleoffice.add(websocket)
                else:
                    print(sysmsgs.BROADCAST_FRNT_SIG0)
                    frontoffice.add(websocket)

            # CONNECTION TEST SIGNALS
            elif m['signal_type'] == 'conn':
                print(sysmsgs.BROADCAST_BACK_SIG2)
                payload = json.dumps(wssmsgs.back_conn_resp)
                for backs in backoffice:
                    await backs.send(payload)

            # TRADE SIGNALS
            elif m['signal_type'] == 'spot_trade':
                for front in frontoffice:
                    await front.send(message)
                print(sysmsgs.BROADCAST_MIDD_SIG2)
                payload = json.dumps(wssmsgs.midl_trde_resp)
                await websocket.send(payload)
                for back in backoffice:
                    await back.send(message)
                for middle in middleoffice:
                    await middle.send(payload)

            elif m['signal_type'] == 'spread_trade':
                for front in frontoffice:
                    await front.send(message)
                print(sysmsgs.BROADCAST_MIDD_SIG2)
                payload = json.dumps(wssmsgs.midl_trde_resp)
                await websocket.send(payload)
                for back in backoffice:
                    await back.send(message)
                for middle in middleoffice:
                    await middle.send(payload)

            elif m['signal_type'] == 'test_trade':
                print(sysmsgs.BROADCAST_BACK_SIG3)
                payload = json.dumps(wssmsgs.back_test_resp)
                for back in backoffice:
                    await back.send(payload)
                for front in frontoffice:
                    await front.send(message)

            else:
                await websocket.send("m")

    except Exception as e:
        print(e)
        print(sysmsgs.BROADCAST_TOTL_SIG1)

    finally:
        if websocket in backoffice:
            backoffice.remove(websocket)
            print(sysmsgs.BROADCAST_BACK_SIG1)
        elif websocket in middleoffice:
            middleoffice.remove(websocket)
            print(sysmsgs.BROADCAST_MIDD_SIG1)
        else:
            frontoffice.remove(websocket)
            print(sysmsgs.BROADCAST_FRNT_SIG1)


def broadcast():
    start_server = websockets.serve(echo, "localhost", PORT)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    broadcast()

