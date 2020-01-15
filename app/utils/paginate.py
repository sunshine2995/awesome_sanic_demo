# -*- coding: utf-8 -*-

import math
from typing import List, Dict

from sqlalchemy import func
from sqlalchemy.orm import Query


class Page:
    def __init__(
        self, content: List, page: int, size: int, total_elements: int
    ) -> None:
        self.content = content
        self.page = page
        self.size = size
        self.total_elements = total_elements
        self.total_pages = math.ceil(total_elements / size)
        self.first = page == 1
        self.last = page == self.total_pages

    def to_dict(self) -> Dict:
        return {
            "content": self.content,
            "page": self.page,
            "size": self.size,
            "total_elements": self.total_elements,
            "total_pages": self.total_pages,
            "first": self.first,
            "last": self.last,
        }


def paginate(query: Query, page: int, size: int) -> Page:
    content: List = query.offset(size * (page - 1)).limit(size).all()
    # https://github.com/pallets/flask-sqlalchemy/pull/281#issuecomment-95957173
    total_elements: int = query.order_by(None).value(func.count())
    return Page(content, page, size, total_elements)
