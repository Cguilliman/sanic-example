import websockets
from aioconsole import ainput
import asyncio


async def recv(ws):
    while True:
        print(await ws.recv())


async def send(ws):
    while True:
        message = await ainput("Input message:")
        await ws.send(message)


async def test():
    uri = "ws://127.0.0.1:9000/chat/3/"
    async with websockets.connect(
        uri, 
        extra_headers={
            "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMCwidXNlcm5hbWUiOiJ1c2VybmFtZTYifQ.RnXZH5kPIZlyL4I5KCr9b2Ua3eFFoqVdVadfEeGCW-U"
        }
    ) as websocket:
        task2 = asyncio.ensure_future(recv(websocket))
        task1 = asyncio.ensure_future(send(websocket))

        done, pending = await asyncio.wait(
            [task2, task1],
            return_when=asyncio.ALL_COMPLETED,
        )

        for task in pending:
            task.cancel()


asyncio.get_event_loop().run_until_complete(test())