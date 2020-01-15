# -*- coding: utf-8 -*-

import asyncio
import hashlib
import random
import secrets
import string
from asyncio import Task
from datetime import datetime, timedelta
from typing import Dict, List

import dateutil.parser
import jwt
import qrcode
from qrcode import QRCode
from qrcode.image.pil import PilImage
from raven import Client
from raven_aiohttp import AioHttpTransport
from sanic.log import logger
from sanic.request import Request

import settings
from settings import SENTRY_DSN, ENV

if ENV == "prod":
    if SENTRY_DSN:
        sentry_client = Client(
            dsn=SENTRY_DSN,
            transport=AioHttpTransport,
            environment=ENV,
            release="latest",
        )
else:
    sentry_client = None


def md5(content: str) -> str:
    return hashlib.md5(content.encode()).hexdigest()


def sha1(content: str) -> str:
    return hashlib.sha1(content.encode()).hexdigest()


def sha256(context: str) -> str:
    return hashlib.sha256(context.encode()).hexdigest()


def generate_token(payload: Dict) -> str:
    ttl: int = 3600 * 24 * 30 * 6
    iat: datetime = datetime.utcnow()
    exp: datetime = datetime.utcnow() + timedelta(seconds=ttl)
    payload.update({"iat": iat, "exp": exp})
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256").decode()


def decode_token(token: str) -> Dict:
    return jwt.decode(token, settings.JWT_SECRET_KEY)


def get_uniqid(length: int) -> str:
    CHARS: str = string.ascii_lowercase + string.digits
    return "".join(secrets.choice(CHARS) for i in range(length))


def get_client_ip(request: Request) -> str:
    if request.remote_addr:
        return request.remote_addr
    return request.ip


def get_current_task() -> Task:
    current_task: Task = asyncio.current_task()
    return current_task


# 生成0.5-1的随机数
def generate_random_number():
    number = random.uniform(5, 10)
    return round(number / 10, 2)


def generate_qrcode(data: str, path: str) -> None:
    qr: QRCode = QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img: PilImage = qr.make_image(fill_color="black", back_color="white")
    img.save(path)


class classproperty(object):
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, obj, cls):
        return self.fget(cls)


def parse_iso8601(date_string: str) -> datetime:
    return dateutil.parser.parse(date_string)


def is_same_day(date1: datetime, date2: datetime) -> bool:
    return date1.strftime("%Y%m%d") == date2.strftime("%Y%m%d")


def is_same_month(date1: datetime, date2: datetime) -> bool:
    return date1.strftime("%Y%m") == date2.strftime("%Y%m")


def generate_discount_limit_key(
    discount_id: int, goods_sku_id: int, user_id: int, subbranch_id: int
) -> str:
    day: str = datetime.now().strftime("%Y-%m-%d")
    key: str = f"day:{day}|discount:{discount_id}|sku:{goods_sku_id}|user:{user_id}|subbranch:{subbranch_id}"
    return key


async def run_tasks(tasks: List) -> None:
    for task in tasks:
        try:
            await task
        except Exception as e:
            logger.error(e)
            send_exception_to_sentry()


def send_exception_to_sentry() -> None:
    if sentry_client:
        sentry_client.captureException()
