from fastapi import APIRouter, Body, Depends, HTTPException
from auth import RoleEnum, get_current_user

from core.user_model import UserBase
from core.common_schema import PaginationModel, PaginationResponse
from db import get_mongo_database, AgnosticDatabase
from core.pagination import MongoDBPagination

router = APIRouter()


@router.post("/", response_model=PaginationResponse)
async def get_list_of_users(
    payload: PaginationModel,
    current_user: UserBase = Depends(
        get_current_user(required_roles=[RoleEnum.admin, RoleEnum.manager])
    ),
    mongo_client: AgnosticDatabase = Depends(get_mongo_database),
):
    """
    Return all users
    """

    pagination = MongoDBPagination(
        mongo_client.users,
        payload.page,
        payload.limit,
        payload.filters,
        payload.sorted_by,
        payload.order_by,
    )

    return await pagination.response_pagination()
