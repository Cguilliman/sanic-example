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
    uri = "ws://127.0.0.1:9000/chat/2/"
    async with websockets.connect(
        uri, 
        extra_headers={"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo3LCJ1c2VybmFtZSI6InVzZXJuYW1lMyJ9.nG_ltG-G9lQrCLYL36pTtu4tA4N_TnoQtSKg-sKgS_Q"}
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