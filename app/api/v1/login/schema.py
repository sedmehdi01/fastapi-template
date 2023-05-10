from pydantic import Field, BaseModel
from auth.role_schema import RoleEnum

from core.common_schema import Response


class LoginPayload(BaseModel):
    username: str = Field(max_length=63)
    password: str = Field(max_length=63)


class CreateAccountPayload(LoginPayload):
    role: RoleEnum


class Token(Response):
    access_token: str
    token_type: str
    refresh_token: str
    user_id: str
