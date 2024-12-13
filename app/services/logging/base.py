from sqlalchemy.orm import DeclarativeBase


class BaseLogModel(DeclarativeBase):
    """Base model."""

    __abstract__ = True
