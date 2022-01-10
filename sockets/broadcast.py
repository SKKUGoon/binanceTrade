import websockets
import asyncio
import json

PORT = 7890

print(f"Server listening on port: {PORT}")

connected = set()

async def echo(websocket, path):
    print("Client Just Connected")
    connected.add(websocket)
    try:
        async for message in websocket:
            print(f"Received message from client {message}")
            m = json.loads(message)

            # CONNECTION TEST SIGNALS
            if m['signal_type'] == 'conn':
                print("[WS] Received connection test message")
                payload = {
                    'signal_type': 'conn_resp',
                    'data': {
                        'status': 'normal',
                        'msg': 'connection_normal'
                    }
                }
                payload_j = json.dumps(payload)
                await websocket.send(payload_j)

            # TESTING SIGNALS
            elif m['signal_type'] == 'trade':
                print("[WS] Received trade messages")
                payload = {
                    'signal_type': 'trade_resp',
                    'data': {
                        'status': 'recieved',
                        'msg': 'successfully recieved'
                    }
                }
                payload_j = json.dumps(payload)
                await websocket.send(payload_j)
            else:
                await websocket.send("m")

    except Exception as e:
        print(e)
        print("A client just disconnected")

    finally:
        connected.remove(websocket)


start_server = websockets.serve(echo, "localhost", PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()