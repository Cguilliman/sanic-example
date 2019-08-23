from typing import Dict

import jwt
from marshmallow import ValidationError

from app.settings import Settings
from .models import User
from shared.crypto import AESCipher

from .serializers import LoginSerializer, RegisterSerializer


class LoginUseCase:
    serializer_class = LoginSerializer

    def __init__(self, data: Dict):
        self.data = data

    async def get_user(self, username):
        return await User.query.where(
            User.username==username
        ).gino.first()

    async def validate(self):
        self.valid_data = self.serializer_class().load(self.data)  # can raise `ValidationError`

        username, password = (
            self.valid_data.get("username"), 
            self.valid_data.get("password")
        )
        self.user = await self.get_user(username)

        if not self.user:
            raise ValidationError(
                "Invalid username or password."
            )

        encoded_password = (
            AESCipher(Settings.SECRET)
            .decrypt(
                self.user.password.encode("utf8")
            )
        )
        if password != encoded_password:
            raise ValidationError(
                "Invalid username or password."
            )

        if not self.user.is_active:
            raise ValidationError(
                "You user is not active, please check email."
            )

    def jwt_token(self):
        payload = self.user.to_dict()
        return jwt.encode(payload, Settings.SECRET, algorithm="HS256")

    async def execute(self):
        # TODO: add login
        await self.validate()
        return self.user, self.jwt_token()


class RegisterUseCase:
    serializer_class = RegisterSerializer

    def __init__(self, data: Dict):
        self.data = data

    async def validate(self):
        self.valid_data = self.serializer_class().load(self.data)

        username, password1, password2 = (
            self.valid_data.get("username"),
            self.valid_data.pop("password1", None),
            self.valid_data.pop("password2", None),
        )

        if password1 != password2:
            raise ValidationError("Password is not the same.")

        if await User.query.where(User.username==username).gino.first():
            raise ValidationError("User with current username is already exists.")    

        self.valid_data["password"] = (
            AESCipher(Settings.SECRET)
            .encrypt(password1)
            .decode("utf8")
        )

    async def execute(self):
        await self.validate()
        # TODO: add email and email confirmation
        return await User.create(
            is_active=True,
            **self.valid_data
        )


def login(data):
    return LoginUseCase(data).execute()


def register(data):
    return RegisterUseCase(data).execute()