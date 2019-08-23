import asyncio
import ujson

import websockets
from aioredis import Channel
from websockets import WebSocketCommonProtocol

from shared.views import authorized
from app.redis import redis_conn_pub
from .models import Room, Message


class ChatManager:
    actions = ["chat"]

    def __init__(self, redis, channel, websocket, room_id, user):
        self.redis = redis
        self.channel = channel
        self.ws = websocket
        self.room_id = room_id
        self.user = user

    @classmethod
    async def initialize(cls, websocket, room_id, user):
        channel = Channel(
            f"channel_{str(room_id)}", 
            is_pattern=False
        )
        return cls(
            await redis_conn_pub.get_redis(),
            channel, websocket, room_id, user
        )

    async def connection_closed(self):
        pass

    async def broadcast(self):
        """Receive messages from redis and send it in users socket"""
        with await self.redis as connection:
            await connection.execute_pubsub("subscribe", self.channel)
            try:
                 while True:
                    message = await self.channel.get(encoding="utf-8")
                    await self.ws.send(message)
            except websockets.ConnectionClosed as e:
                print(f"<ChatManager:broadcast>[error] {e}")
                await self.connection_closed()

    def decode_message(self, received):
        return "chat", received

    async def handle(self):
        try:
            while True:
                action, data = self.decode_message(await self.ws.recv())
                # TODO: action invalidation
                func = getattr(self, action)
                await func(data)
        except websockets.ConnectionClosed as e:
            print(f"<ChatManager:handle>[error] {e}")
            await self.connection_closed()

    async def chat(self, message):
        with await self.redis as connection:
            await Message.create(
                message=message,
                room=self.room_id,
                from_user=self.user.id,
            )
            await connection.execute(
                "publish", self.channel.name, message
            )


@authorized
async def chat(request, ws, *args, **kwargs):
    try:
        pk = int(kwargs.get("pk"))
    except ValueError:
        return

    room = await Room.query.where(Room.id==int(kwargs.get("pk"))).gino.first()

    if not room:
        return

    chat = await ChatManager.initialize(
        ws, room.id, request.get("user")
    )

    handle_task = asyncio.ensure_future(chat.handle())
    broadcast_task = asyncio.ensure_future(chat.broadcast())

    done, pending = await asyncio.wait(
        [handle_task, broadcast_task],
        return_when=asyncio.FIRST_COMPLETED
    )

    for task in pending:
        task.cancel()
