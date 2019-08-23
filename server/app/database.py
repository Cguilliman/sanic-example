from gino.ext.sanic import Gino


DB = Gino()


def init_database(app):
    global DB
    DB.init_app(app)


def get_alembic_db():
    global DB
    from users.models import User
    from chat.models import Room, UserRoom, Message
    return DB
