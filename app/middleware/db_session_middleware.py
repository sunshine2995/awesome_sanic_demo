# -*- coding: utf-8 -*-

from sanic import Sanic
from sanic.request import Request

from app.database import Session


async def create_db_session_middleware(request: Request) -> None:
    Session()


async def remove_db_session_middleware(request, response) -> None:
    Session.remove()


def install(app: Sanic) -> None:
    app.request_middleware.append(create_db_session_middleware)
    app.response_middleware.append(remove_db_session_middleware)
