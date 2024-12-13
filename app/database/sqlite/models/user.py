from sqlalchemy import Boolean, Column, String

from app.database.sqlite.base import BaseModel


class User(BaseModel):
    __tablename__ = "user"
    username = Column(String(50), nullable=False, unique=True, index=True)
    password = Column(String(50), nullable=False)
    is_active = Column(Boolean(), nullable=False, default=True)
