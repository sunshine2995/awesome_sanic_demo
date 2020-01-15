# -*- coding: utf-8 -*-

from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse, text, json

from app import create_app

app: Sanic = create_app()


@app.route("/favicon.ico")
async def get_favicon(request: Request) -> HTTPResponse:
    return json({"code": 404, "message": "favicon.icon not found"}, status=404)


@app.route("/ping", methods=["GET", "HEAD"])
async def ping(request: Request) -> HTTPResponse:
    return text("pong")


@app.route("/ip", methods=["GET"])
async def get_my_ip(request: Request) -> HTTPResponse:
    return json({"ip": request["ip"]})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=18100, debug=False)
