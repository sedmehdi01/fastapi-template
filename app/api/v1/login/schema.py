from pydantic import Field, BaseModel
from typing import Optional

from core.common_schema import Response


class LoginPayload(BaseModel):
    username: str = Field(max_length=63)
    password: str = Field(max_length=63)


class Token(Response):
    access_token: str
    token_type: str
    refresh_token: str
    user_id: str
