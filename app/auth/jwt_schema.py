from pydantic import BaseModel

from .role_schema import RoleEnum


class DataJWT(BaseModel):
    user_id: str
    role: RoleEnum
