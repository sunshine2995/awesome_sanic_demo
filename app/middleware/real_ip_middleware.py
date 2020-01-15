# -*- coding: utf-8 -*-

from sanic import Sanic
from sanic.request import Request

from app.utils import get_client_ip


async def real_ip_middleware(request: Request) -> None:
    ip: str = get_client_ip(request)
    request["ip"] = ip


def install(app: Sanic) -> None:
    app.request_middleware.append(real_ip_middleware)
