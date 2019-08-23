from sanic.exceptions import abort


def authorized(func):
    async def wrapped(request, *args, **kwargs):
        user = request.get("user")
        if user and user.is_authenticated():
            return await func(request, *args, **kwargs)
        return abort(403)
    return wrapped
