from typing import Optional
from pydantic import BaseModel, Field, field_validator
from uuid import UUID


class CreateCommandSchema(BaseModel):
    id: UUID = Field(..., alias="id")
    type: str = Field(..., alias="type")
    status: str = Field(..., alias="status")
    data: Optional[dict] = Field(None, alias="data")
    mode: str = Field(..., alias="mode")

    @field_validator("status", mode="before")
    @classmethod
    def validate_status(cls, value):
        value = value.lower()
        if value not in CommandStatusEnum.__dict__.values():
            raise ValueError(f"Invalid status: {value}")
        return value


class CommandReceiveSchema(BaseModel):
    id: UUID
    type: str
    data: Optional[dict] = None
    mode: str
    status: Optional[str] = Field(None)
    created_at: Optional[str] = Field(None)
    updated_at: Optional[str] = Field(None)

    def model_dump(self):
        return {
            "id": self.id,
            "type": self.type,
            "data": self.data,
            "mode": self.mode,
        }


class CommandUpdateSchema(BaseModel):
    status: str
    data: Optional[dict] = None

    def model_dump(self):
        return {
            "status": self.status,
            "data": self.data,
        }


class CommandStatusEnum:
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILED = "failed"
