# -*- coding: utf-8 -*-

import json
import time
from datetime import datetime
from decimal import Decimal

from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if hasattr(obj, "to_dict"):
            return obj.to_dict()
        if isinstance(obj, Decimal):
            return str(obj)
        return super().default(obj)


def to_json(response) -> str:
    return json.dumps(response, cls=CustomJSONEncoder)


async def stats_middleware_start_timer(request: Request) -> None:
    if request.method == "OPTIONS":
        return

    request["start_time"] = time.time()


async def response_body_middleware(request: Request, response: HTTPResponse):
    if request.method == "OPTIONS":
        return

    if not isinstance(response, HTTPResponse):
        json_response: str = to_json({"code": 200, "message": "请求成功", "data": response})
        response = HTTPResponse(json_response, content_type="application/json")

    start_time = request.get("start_time")
    if start_time:
        duration = time.time() - start_time
        response.headers["X-Duration-Time"] = int(duration * 1000)

    response.headers["Server"] = "nginx/1.14.0 (Ubuntu)"
    return response


def install(app: Sanic) -> None:
    app.request_middleware.append(stats_middleware_start_timer)
    app.response_middleware.append(response_body_middleware)
