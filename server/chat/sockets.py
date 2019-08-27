import asyncio
import ujson

import websockets
from aioredis import Channel
from websockets import WebSocketCommonProtocol
from marshmallow import Schema, fields

from shared.views import authorized
from app.redis import redis_conn_pub
from .models import Room, Message, UserRoom


# {
#     "action": "message.new" | "error" | "user_status",
#     "data": {
#         "room_id": "room_id"
#         "from_user": "user id"      | -               | "user id",
#         "data": "Some message" | "error message" | "online|offline"
#     }
# }


class MessageSchema(Schema):
    room_id = fields.Int()
    from_user = fields.Int()
    data = fields.Str()


def generate_channel_name(user_id):
    return f"user_channel_{user_id}",


class SocketManager:
    actions = {
        "message.new": ("new_message", MessageSchema)
    }

    def __init__(self, redis, channel, websocket, user):
        self.redis = redis
        self.channel = channel
        self.ws = websocket
        self.user = user

    @classmethod
    async def initialize(cls, websocket, user):
        channel = Channel(
            generate_channel_name(user.id),
            is_pattern=False
        )

        return cls(
            await redis_conn_pub.get_redis(),
            channel, 
            websocket, 
            user
        )

    async def connection_closed(self):
        # TODO send user status message in socket
        pass

    async def broadcast(self):
        """Receive messages from redis and send it in users socket"""
        with await self.redis as connection:
            await connection.execute_pubsub("subscribe", self.channel)
            try:
                 while True:
                    room = await self.channel.get(encoding="utf-8")
                    await self.ws.send(message)
            except websockets.ConnectionClosed as e:
                print(f"<ChatManager:broadcast>[error] {e}")
                await self.connection_closed()

    async def validate_action(self, received):
        schema = ujson.loads(received)
        action, schema = self.actions.get(schema.get("action"), (None, None))
        if action:
            return action, schema
        # TODO: raise socket error
        return "chat", None

    async def handle(self):
        try:
            while True:
                received = await self.ws.recv()
                action, schema = await self.validate_action(received)
                data = schema().load(received)
                # TODO: action invalidation
                func = getattr(self, action)
                await func(data)
        except websockets.ConnectionClosed as e:
            print(f"<ChatManager:handle>[error] {e}")
            await self.connection_closed()

    async def new_message(self, data):
        message = await Message.create(
            message=data.get("data"),
            room=data.get("room_id"),
            from_user=data.get("from_user"),
        )
        with await self.redis as connection:
            for user_id in self.room_users:
                await connection.execute(
                    "publish", 
                    generate_channel_name(user_id), 
                    message
                )


# TODO: add socket error message before break connection
@authorized
async def personal(request, ws, *args, **kwargs):
    user = request.get("user")

    chat = await SocketManager.initialize(
        ws, request.get("user")
    )

    handle_task = asyncio.ensure_future(chat.handle())
    broadcast_task = asyncio.ensure_future(chat.broadcast())

    done, pending = await asyncio.wait(
        [handle_task, broadcast_task],
        return_when=asyncio.FIRST_COMPLETED
    )

    for task in pending:
        task.cancel()
