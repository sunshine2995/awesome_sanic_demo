# -*- coding: utf-8 -*-

from sqlalchemy import Column, BigInteger, String

from app.database import Base


class Demo(Base):
    __tablename__ = "demo"

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="主键")
    desc = Column(String, default="", comment="描述")
