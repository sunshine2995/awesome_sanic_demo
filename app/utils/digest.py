# -*- coding: utf-8 -*-

import hashlib


def _md5(content: bytes) -> str:
    return hashlib.md5(content).hexdigest()
