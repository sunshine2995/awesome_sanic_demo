# -*- coding: utf-8 -*-

from typing import List

from app.database import Session
from app.demo.demo_type import RequestDemoType
from app.demo.model import Demo
from app.exceptions import DemoNotExist


def get_demos() -> List[Demo]:
    session: Session = Session()
    demos: List[Demo] = session.query(Demo).all()
    return demos


def get_demo_by_id(demo_id: int) -> Demo:
    session: Session = Session()
    demo: Demo = session.query(Demo).filter(Demo.id == demo_id).first()
    if not demo:
        raise DemoNotExist()
    return demo


def add_demo(request_body: RequestDemoType) -> Demo:
    desc: str = request_body.get("desc")
    demo = Demo()
    demo.desc = desc
    return demo


def update_demo(demo_id: int, request_body: RequestDemoType) -> Demo:
    demo: Demo = get_demo_by_id(demo_id)
    demo.desc = request_body.get("desc")
    return demo
