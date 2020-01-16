# -*- coding: utf-8 -*-

from typing import List, Dict

from app.database import get_transactional_id, Session, transactional
from app.demo import repository as demo_repo
from app.demo.demo_type import RequestDemoType
from app.demo.model import Demo


async def get_demos() -> List[Demo]:
    return demo_repo.get_demos()


async def get_demo_by_id(demo_id: int) -> Demo:
    return demo_repo.get_demo_by_id(demo_id)


@get_transactional_id
def get_add_demo_id(request_body: RequestDemoType):
    return demo_repo.add_demo(request_body)


async def add_demo(request_body: RequestDemoType) -> Demo:
    demo_id = get_add_demo_id(request_body)
    return await get_demo_by_id(demo_id)


@get_transactional_id
def get_update_demo_id(demo_id: int, request_body: RequestDemoType):
    return demo_repo.update_demo(demo_id, request_body)


async def update_demo(demo_id: int, request_body: RequestDemoType) -> Demo:
    demo_id: int = get_update_demo_id(demo_id, request_body)
    return await get_demo_by_id(demo_id)


@transactional
async def delete_demo(demo_id: int) -> Dict:
    session = Session()
    demo: Demo = demo_repo.get_demo_by_id(demo_id)
    session.delete(demo)
    return {"message": "删除成功"}
