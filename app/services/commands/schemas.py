from enum import StrEnum
from typing import Optional

from pydantic import BaseModel


class CommandReceiveSchema(BaseModel):
    type: str
    id: str
    data: Optional[dict] = None


class CommandStatusEnum(StrEnum):
    IN_PROGRESS = "IN_PROGRESS"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

    # def __str__(self):
    #     return self.value
