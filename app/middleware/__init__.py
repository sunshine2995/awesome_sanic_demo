# -*- coding: utf-8 -*-

from sanic import Sanic

import settings
from app.middleware import (
    signature_middleware,
    db_session_middleware,
    jwt_authentication_middleware,
    real_ip_middleware,
    response_body_middleware,
)


def configure_middlewares(app: Sanic) -> None:
    real_ip_middleware.install(app)

    if settings.ENV == "prod":
        signature_middleware.install(app)

    db_session_middleware.install(app)
    jwt_authentication_middleware.install(app)
    response_body_middleware.install(app)
