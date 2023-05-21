from enum import Enum
from pydantic import BaseModel


class RoleEnum(str, Enum):
    admin = "admin"
    manager = "manager"
    support = "support"
    user = "user"


class TokenType(str, Enum):
    ACCESS = "access_token"
    REFRESH = "refresh_token"


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
    user_id: str
