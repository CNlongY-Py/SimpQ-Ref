import asyncio
import websockets
import index


async def hello(data):
    async with websockets.connect(index.send_host) as websocket:
        return await websocket.send(data)


def send(data):
    return asyncio.run(hello(data))
