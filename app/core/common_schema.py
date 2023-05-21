from pydantic import BaseModel
from enum import Enum
from typing import Optional


class OrderByColumn(int, Enum):
    ASCENDING = 1
    DESCENDING = -1


class PaginationMetaData(BaseModel):
    count: int
    next: Optional[int] = None
    previous: Optional[int] = None


class PaginationModel(BaseModel):
    page: Optional[int] = 1
    limit: Optional[int] = 20
    filters: Optional[dict] = {}
    sorted_by: Optional[str] = None
    order_by: Optional[OrderByColumn] = 1


class PaginationResponse(BaseModel):
    meta: PaginationMetaData
    data: list[dict]
