from fastapi import APIRouter, Body, Depends, HTTPException
from auth.role_schema import RoleEnum
from auth.deps import get_current_user

from core.user_model import UserBase
from db import get_mongo_database, AgnosticDatabase
from core.utils import obj_to_str

router = APIRouter()

@router.get("/")
async def get_list_of_users(
    current_user: UserBase = Depends(
        get_current_user(
            required_roles=[RoleEnum.admin, RoleEnum.manager]
        )
    ),
    mongo_client: AgnosticDatabase = Depends(get_mongo_database),
):
    """
    Return all users
    """

    users = list()
    async for user in mongo_client.users.find():
        print(user)
        users.append(user)

    return obj_to_str(users)
