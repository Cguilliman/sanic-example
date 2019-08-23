import os


class Settings:
    HOST = os.environ.get("HOST", "0.0.0.0")
    PORT = os.environ.get("PORT", "9000")
    DEBUG = os.environ.get("DEBUG", True)
    DB_USER = os.environ.get("DATABASE_USER", "postgres")
    DB_PASSWORD = os.environ.get("DATABASE_PASSWORD", "postgres")
    DB_DATABASE = os.environ.get("DATABASE_NAME", "sanic_example")
    DB_HOST = os.environ.get("DATABASE_HOST", "localhost")
    SECRET = os.environ.get("SECRET", "secret")
    JWT_SECRET = os.environ.get("JWT_SECRET", "jwt_secret")


class RedisSettings:
    HOSTNAME = os.environ.get("REDIS_HOST", "localhost")
    PORT = os.environ.get("REDIS_PORT", 6379)
