from enum import StrEnum
from typing import Optional

from pydantic import BaseModel
from uuid import UUID


class CommandReceiveSchema(BaseModel):
    type: str
    id: UUID
    data: Optional[dict] = None


class CommandStatusEnum(StrEnum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

    # def __str__(self):
    #     return self.value
