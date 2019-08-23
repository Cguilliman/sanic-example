from marshmallow import Schema, fields


class LoginSerializer(Schema):
    username = fields.Str()
    password = fields.Str()


class RegisterSerializer(Schema):
    username = fields.Str()
    password1 = fields.Str()
    password2 = fields.Str()


class UserSerializer(Schema):
    id = fields.Int()
    username = fields.Str()
