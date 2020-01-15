# -*- coding: utf-8 -*-

from sanic import Sanic
from sanic.request import Request

import settings
from app.exceptions import BadRequest
from app.utils import md5
from settings import APP_KEY


def generate_signature(timestamp: str) -> str:
    return md5(f"{timestamp}.{APP_KEY}")


async def signature_middleware(request: Request) -> None:
    path: str = request.path

    if path in settings.SIGNATURE_WHITE_LIST:
        return

    timestamp: str = request.headers.get("Timestamp")
    signature: str = request.headers.get("Signature")
    if timestamp is None or signature is None:
        raise BadRequest()

    expect_signature: str = generate_signature(timestamp)
    if signature != expect_signature:
        raise BadRequest()


def install(app: Sanic) -> None:
    app.request_middleware.append(signature_middleware)
