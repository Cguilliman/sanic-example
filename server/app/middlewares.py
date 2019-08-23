import jwt

from sanic.request import Request

from .settings import Settings
from users.models import User


def session_middleware_request(request: Request):
    print(request)


def session_middleware_response(request, response):
    print(response)


async def jwt_user_middleware_request(request: Request):
    header = request.headers.get("authorization")
    if not header:
        return
    prefix, token = header.split(" ")
    payload = jwt.decode(token, Settings.SECRET, algorithms=['HS256'])
    user = (
        await User.query
        .where(
            User.username==payload.get("username", None)
            and User.id==payload.get("user_id", 0))
        .gino.first()
    )
    if user:
        request["user"] = user


def init_middlewares(app):
    app.register_middleware(jwt_user_middleware_request, "request")
    # app.register_middleware(session_middleware_response, "response")
