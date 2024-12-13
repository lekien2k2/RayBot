from sqlalchemy import Boolean, Column, String

from app.database.sqlite.base import BaseModel


class Logs(BaseModel):
    __tablename__ = "logs"
    username = Column(String(50), nullable=False)
    action = Column(String(50), nullable=False)
    time = Column(String(50), nullable=False)
    status = Column(Boolean(), nullable=False)
    message = Column(String(50), nullable=False)
