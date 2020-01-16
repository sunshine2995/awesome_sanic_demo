# -*- coding: utf-8 -*-

from traceback import format_exc
from typing import Dict

from sanic import Sanic
from sanic.exceptions import SanicException
from sanic.handlers import ErrorHandler
from sanic.log import logger
from sanic.request import Request
from sanic.response import HTTPResponse, json

from app.exceptions import AuthenticationFailed, BadRequest, NoToken, DemoNotExist
from app.utils import send_exception_to_sentry


class CustomHandler(ErrorHandler):
    def response(self, request, exception):
        self.log(format_exc())
        send_exception_to_sentry()
        return super().response(request, exception)

    def log(self, message, level="error"):
        getattr(logger, level)(message)

    def default(self, request: Request, exception: Exception) -> HTTPResponse:
        if issubclass(type(exception), SanicException):
            status: int = getattr(exception, "status_code")
            body: Dict = {"code": status, "message": "Error: {}".format(exception)}
            return json(body, status=status)
        return json({"code": 500, "message": "内部服务器错误"}, status=500)


def handle_bad_request(request, exception) -> HTTPResponse:
    return json({"code": 40000, "message": "Bad Request"}, status=400)


def handle_no_token(request, exception) -> HTTPResponse:
    return json({"code": 40100, "message": "用户鉴权失败，请重新登陆"}, status=401)


def handle_authentication_failed(request, exception) -> HTTPResponse:
    return json({"code": 40300, "message": "认证失败"}, status=403)


def handle_demo_not_exist(request, exception) -> HTTPResponse:
    return json({"code": 41001, "message": "Demo不存在"}, status=400)


def configure_exception_handlers(app: Sanic) -> None:
    app.error_handler.add(BadRequest, handle_bad_request)
    app.error_handler.add(NoToken, handle_no_token)
    app.error_handler.add(AuthenticationFailed, handle_authentication_failed)
    app.error_handler.add(DemoNotExist, handle_demo_not_exist)
