from pydantic import Field, BaseModel
from auth.role_schema import RoleEnum


class LoginPayload(BaseModel):
    username: str = Field(max_length=63)
    password: str = Field(max_length=63)


class CreateAccountPayload(LoginPayload):
    role: RoleEnum
