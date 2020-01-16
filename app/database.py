# -*- coding: utf-8 -*-

import functools
from typing import Dict, List

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

import settings
from app.utils import get_current_task, classproperty


class MyBase(object):
    def to_dict(self) -> Dict:
        fields: List = getattr(self, "__fields__", None)
        if not fields:
            fields = self.__table__.columns.keys()
        return {key: getattr(self, key) for key in fields}

    def values(self, filter_list: List[str]) -> Dict:
        return {key: getattr(self, key) for key in filter_list}

    @classproperty
    def query(cls):
        return Session().query(cls)

    @classmethod
    def with_for_update(cls):
        return Session().query(cls).with_for_update()

    @classmethod
    def from_dict(cls, kwargs):
        return cls(**kwargs)

    @classmethod
    def get(cls, pk):
        return Session().query(cls).get(pk)

    def save(self):
        Session().commit()

    def delete(self):
        Session().delete(self)


Base = declarative_base(cls=MyBase)


engine: Engine = create_engine(
    settings.DB_SETTINGS["dsn"],
    pool_size=settings.DB_SETTINGS["pool_size"],
    pool_recycle=settings.DB_SETTINGS["pool_recycle"],
    max_overflow=settings.DB_SETTINGS["max_overflow"],
    pool_pre_ping=True,
    echo=False,
)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory, scopefunc=get_current_task)


def transactional(f):
    @functools.wraps(f)
    async def wrapper(*args, **kwargs):
        rv = await f(*args, **kwargs)
        Session().commit()
        return rv

    return wrapper


def get_transactional_id(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        rv = f(*args, **kwargs)
        Session().add(rv)
        Session().commit()
        return rv.id

    return wrapper
