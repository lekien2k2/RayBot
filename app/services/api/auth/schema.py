from pydantic import BaseModel, Field


class JwtData(BaseModel):
    user_id: int = Field(alias="sub")
    username: str = Field(alias="username")
    role: str = Field(alias="role")


class LoginRequest(BaseModel):
    username: str = Field(min_length=4, max_length=30)
    password: str = Field(min_length=4, max_length=30)


class LoginResponse(BaseModel):
    access_token: str
    role: str
