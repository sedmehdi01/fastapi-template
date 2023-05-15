from pydantic import BaseModel
from enum import Enum


class TokenType(str, Enum):
    ACCESS = "access_token"
    REFRESH = "refresh_token"


class Response(BaseModel):
    message: str


class Token(Response):
    access_token: str
    token_type: str
    refresh_token: str
    user_id: str
