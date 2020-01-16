# -*- coding: utf-8 -*-

import aio_pika
from aio_pika import Connection, Channel
from aioredis import Redis, create_redis_pool
from sanic import Sanic
from sanic_cors import CORS

import settings
from app.utils.http import create_aiohttp_session, close_aiohttp_session
from app.middleware import configure_middlewares
from app.exception_handlers import configure_exception_handlers, CustomHandler
from app.demo.view import demo_blueprint


async def setup_redis(app: Sanic, loop) -> None:
    app.redis: Redis = await create_redis_pool(
        settings.REDIS_DSN, encoding="utf8", minsize=5, maxsize=10
    )
    app.redis_bytes: Redis = await create_redis_pool(
        settings.REDIS_DSN, minsize=5, maxsize=10
    )


async def setup_amqp(app: Sanic, loop) -> None:
    connection: Connection = await aio_pika.connect_robust(settings.AMQP_URL)
    channel: Channel = await connection.channel()
    app.amqp_connection = connection
    app.amqp_channel = channel


async def close_amqp(app: Sanic, loop) -> None:
    await app.amqp_connection.close()


async def setup_http_session(app: Sanic, loop) -> None:
    await create_aiohttp_session()


async def close_http_session(app: Sanic, loop) -> None:
    await close_aiohttp_session()


async def close_redis(app: Sanic, loop) -> None:
    app.redis.close()
    await app.redis.wait_closed()
    app.redis_bytes.close()
    await app.redis_bytes.wait_closed()


def configure_blueprints(app: Sanic) -> None:
    app.blueprint(demo_blueprint, url_prefix="/demo")


def configure_listeners(app: Sanic) -> None:
    app.register_listener(setup_redis, "before_server_start")
    app.register_listener(setup_http_session, "before_server_start")
    app.register_listener(setup_amqp, "before_server_start")
    app.register_listener(close_redis, "after_server_stop")
    app.register_listener(close_http_session, "after_server_stop")
    app.register_listener(close_amqp, "after_server_stop")


def create_app() -> Sanic:
    error_handler = CustomHandler()
    app: Sanic = Sanic(error_handler=error_handler)
    app.config.PROXIES_COUNT = settings.PROXIES_COUNT
    configure_blueprints(app)
    configure_listeners(app)
    configure_middlewares(app)
    configure_exception_handlers(app)
    CORS(app, automatic_options=True)
    return app
