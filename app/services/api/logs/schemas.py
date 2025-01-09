from pydantic import BaseModel, Field


class CreateLogSchema(BaseModel):
    username: str = Field(..., description="Username")
    action: str = Field(..., description="Action")
    time: str = Field(..., description="Time")
    status: str = Field(..., description="Status")
    message: str = Field(..., description="Message")


class LogSchema(BaseModel):
    id: int
    username: str
    action: str
    time: str
    status: str
    message: str
