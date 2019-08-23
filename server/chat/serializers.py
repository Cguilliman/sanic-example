from marshmallow import Schema, fields

from users.serializers import UserSerializer


class MessageSerializer(Schema):
    id = fields.Int()
    message = fields.Str()
    from_user = fields.Int()
    created_at = fields.DateTime()


class RoomSerializer(Schema):
    id = fields.Int()
    title = fields.Str()


class RoomCreateSerializer(Schema):
    user = fields.Int()
