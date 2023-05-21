from pydantic import Field, BaseModel
from auth import RoleEnum


class LoginPayload(BaseModel):
    username: str = Field(max_length=63)
    password: str = Field(max_length=63)


class CreateAccountPayload(LoginPayload):
    role: RoleEnum
