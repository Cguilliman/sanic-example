from sanic import response
from sanic.request import Request

from marshmallow import ValidationError

from shared.views import authorized
from .models import User
from .serializers import UserSerializer
from . import usecases


async def main(request, *args, **kwargs):
    return response.json({"status": "OK"})


async def login(request, *args, **kwargs):
    try:
        user, token = await usecases.login(request.json)
    except ValidationError as e:
        # TODO: re-factor errors raising
        return response.json({"errors": e.args})
    return response.json({
        "data": {
            "id": user.id,
            "username": user.username,
            "token": token,
        }
    })


async def register(request, *args, **kwargs):
    try:
        user = await usecases.register(request.json)
    except ValidationError as e:
        # TODO: re-factor errors raising
        return response.json({"errors": e.args})
    return response.json({
        "data": {
            "id": user.id,
            "username": user.username,
        }
    })


@authorized
async def receive(request, *args, **kwargs):
    return response.json({
        "data": UserSerializer().dump(request.get("user"))
    })
