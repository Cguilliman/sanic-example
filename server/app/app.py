from sanic import Sanic
from environs import Env

from .settings import Settings
from .database import init_database
from .routers import init_routers
from .middlewares import init_middlewares
from .sockets import init_ws
from .redis import redis_conn_pub, redis_conn_sub


app = Sanic(__name__)


@app.listener('before_server_start')
async def start_redis(app, loop):
    await redis_conn_pub.connect()
    await redis_conn_sub.connect()


@app.listener('after_server_stop')
async def end_redis(app, loop):
    await redis_conn_pub.close()
    await redis_conn_sub.close()


def init():
    env = Env()
    env.read_env()

    app.config.from_object(Settings)
    
    init_database(app)
    init_routers(app)
    init_middlewares(app)
    init_ws(app)

    app.run(
        host=app.config.HOST,
        port=app.config.PORT,
        debug=app.config.DEBUG,
        auto_reload=app.config.DEBUG,
    )
