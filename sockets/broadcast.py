import websockets
import asyncio


PORT = 7890

print(f"Server listening on port: {PORT}")

async def echo(websocket, path):
    print("Client Just Connected")

    try:
        async for message in websocket:
            print(f"Received message from clien {message}")
            await websocket.send(f"Pong: {message}")

    except Exception as e:
        print(e)
        print("A client just disconnected")


start_server = websockets.serve(echo, "localhost", PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()