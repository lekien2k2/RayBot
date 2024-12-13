from sqlalchemy import BIGINT, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
