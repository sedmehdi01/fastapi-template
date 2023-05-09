from uuid import UUID
from pydantic import BaseModel, validator
from enum import Enum


class TokenType(str, Enum):
    ACCESS = "access_token"
    REFRESH = "refresh_token"


class Response(BaseModel):
    message: str
