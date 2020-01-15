# -*- coding: utf-8 -*-

import json
from typing import Dict

import aiohttp

from settings import HTTP_TIMEOUT

aiohttp_session = None


async def create_aiohttp_session():
    global aiohttp_session
    connector = aiohttp.TCPConnector(verify_ssl=False)
    aiohttp_session = aiohttp.ClientSession(connector=connector)


async def close_aiohttp_session():
    global aiohttp_session
    await aiohttp_session.close()


async def http_get_text(url: str, encoding=None) -> str:
    async with aiohttp_session.get(url, timeout=HTTP_TIMEOUT) as response:
        text: str = await response.text(encoding)
        return text


async def http_get_json(url: str) -> Dict:
    text: str = await http_get_text(url)
    return json.loads(text)


async def http_post_xml(url: str, data: str) -> str:
    headers: Dict[str, str] = {"content-type": "text/xml"}
    async with aiohttp_session.post(
        url, data=data, headers=headers, timeout=HTTP_TIMEOUT
    ) as response:
        text: str = await response.text()
        return text


async def http_post_json(url: str, data: Dict) -> Dict:
    async with aiohttp_session.post(url, json=data, timeout=HTTP_TIMEOUT) as response:
        return await response.json()


async def http_post_form(url: str, data: Dict) -> str:
    async with aiohttp_session.post(url, data=data, timeout=HTTP_TIMEOUT) as response:
        text: str = await response.text()
        return text
