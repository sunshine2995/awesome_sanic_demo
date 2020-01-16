# -*- coding: utf-8 -*-

from typing import List, Dict

from sanic import Blueprint
from sanic.request import Request

from app.demo import service as demo_service
from app.demo.model import Demo

demo_blueprint = Blueprint("demo", __name__, version="v1")


@demo_blueprint.route("", methods=["GET"])
async def get_demos(request: Request) -> List[Demo]:
    return await demo_service.get_demos()


@demo_blueprint.route("/one", methods=["GET"])
async def get_demo_by_id(request: Request) -> Demo:
    demo_id: int = int(request.args.get("demo_id"))
    return await demo_service.get_demo_by_id(demo_id)


@demo_blueprint.route("", methods=["POST"])
async def add_demo(request: Request) -> Demo:
    request_body = request.json
    return await demo_service.add_demo(request_body)


@demo_blueprint.route("", methods=["PUT"])
async def update_demo(request: Request) -> Demo:
    demo_id: int = int(request.args.get("id"))
    request_body = request.json
    return await demo_service.update_demo(demo_id, request_body)


@demo_blueprint.route("", methods=["DELETE"])
async def delete_demo(request: Request) -> Dict:
    demo_id: int = int(request.args.get("id"))
    return await demo_service.delete_demo(demo_id)
