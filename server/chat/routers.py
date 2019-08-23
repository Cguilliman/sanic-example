from sanic import response
from sanic.exceptions import abort

from marshmallow import ValidationError

from shared.views import authorized
from users.models import User
from .models import Message, Room, UserRoom
from .serializers import (
    MessageSerializer, 
    RoomSerializer, 
    RoomCreateSerializer
)
from app.redis import redis_conn_pub


@authorized
async def room_messages(request, *args, **kwargs):
    try:
        pk = int(kwargs.get("pk"))
    except ValueError:
        return abort(404)

    user_relation = (
        await UserRoom.query
        .where(
            UserRoom.user==request["user"].id 
            and UserRoom.room==pk)
        .gino.first()
    )
    if not user_relation:
        return abort(404)

    room = await Room.query.where(Room.id==pk).gino.first()
    if not room:
        return abort(404)

    room = RoomSerializer().dump(room)

    # get page GET parameter for pagination
    # TODO: re-factor
    try:
        page = int(request.get_args().get("page", ["1"])[0])
        page = 1 if page <= 0 else page
    except ValueError:
        page = 1
    
    messages = (
        await Message.query
        .limit(10)
        .offset(10*page-10)
        .where(Message.room==pk)
        .gino.all()
    )
    room['messages'] = MessageSerializer(many=True).dump(messages)

    return response.json({"status": "OK", "data": room})


@authorized
async def create_room(request, *args, **kwargs):
    try:
        validated_data = RoomCreateSerializer().load(request.json)
    except ValidationError as e:
        return response.json({"errors": e.args}, 400)

    opponent_user = (
        await User.query
        .where(
            User.id==validated_data["user"])
        .gino.first()
    )
    if not opponent_user:
        return response.json({"errors": "Unknown user"}, 400)

    room = await Room.create(
        title="-",
    )
    await UserRoom.create(user=request["user"].id, room=room.id)
    await UserRoom.create(user=validated_data["user"], room=room.id)

    return response.json({"status": "OK", "data": room.id})
