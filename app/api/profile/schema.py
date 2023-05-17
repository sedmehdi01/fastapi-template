from enum import Enum
from typing import Optional
from pydantic import BaseModel


class Birthday(BaseModel):
    year: int
    month: int
    day: int


class Gender(str, Enum):
    unknown = "unknown"
    male = "male"
    female = "female"
    other = "other"


class Profile(BaseModel):
    fist_name: Optional[str] = None
    last_name: Optional[str] = None
    birthday: Optional[Birthday] = None
    gender: Optional[Gender] = Gender.unknown
    # email: Optional[str] = None
    # phone_number: Optional[int] = None
