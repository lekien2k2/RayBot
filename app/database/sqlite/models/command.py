from sqlalchemy import Column, String, JSON, DateTime, func

from app.database.sqlite.base import Base
from sqlalchemy.dialects.postgresql import UUID


class Command(Base):
    __tablename__ = "command"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
    )
    type = Column(String, index=True)
    status = Column(String)
    data = Column(JSON)
    mode = Column(String)
    created_at = Column(
        DateTime,
        default=func.now(),
        nullable=False,
    )
    updated_at = Column(
        DateTime,
        onupdate=func.now(),
    )
