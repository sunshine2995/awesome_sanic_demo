# -*- coding: utf-8 -*-

from typing import Dict

from jwt import PyJWTError
from sanic import Sanic
from sanic.request import Request

import settings
from app.exceptions import NoToken
from app.utils import decode_token


def get_token_or_raise(request: Request) -> str:
    token: str = request.token
    if token is None:
        raise NoToken()
    return token


async def jwt_authentication_middleware(request: Request) -> None:
    path: str = request.path

    if path in settings.WHITE_LIST:
        return

    token: str = get_token_or_raise(request)
    payload: Dict = decode_token(token)
    user_id: int = payload["user_id"]
    # 解析用户 处理token逻辑


def install(app: Sanic) -> None:
    app.request_middleware.append(jwt_authentication_middleware)
