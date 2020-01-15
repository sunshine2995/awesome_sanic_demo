# -*- coding: utf-8 -*-

import os

# dev/test/prod
ENV = os.environ.get("ENV", "dev")

# https://sanic.readthedocs.io/en/latest/sanic/config.html#about-proxy-servers-and-client-ip
PROXIES_COUNT: int = int(os.environ.get("PROXIES_COUNT", "0"))

# mysql
DB_SETTINGS = {
    "dsn": os.environ.get(
        "DB_DSN",
        "mysql+pymysql://root:root@127.0.0.1:3306/character_test?charset=utf8mb4",
    ),
    "pool_size": 100,
    "pool_recycle": 1200,
    "max_overflow": 10,
}

REDIS_DSN = os.environ.get("REDIS_DSN", "redis://127.0.0.1:6379")

AMQP_URL = os.environ.get("AMQP_URL", "amqp://guest:guest@127.0.0.1:5672/")

WHITE_LIST = [
    "/favicon.ico",
    "/ping",
    "/ip",
]

APP_KEY = "Demo_7456"

SIGNATURE_WHITE_LIST = []

# jwt token
JWT_SECRET_KEY = "demo_secret"

# http request timeout
HTTP_TIMEOUT = 5

SENTRY_DSN = {}
