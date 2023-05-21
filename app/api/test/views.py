from fastapi import APIRouter, Body, Depends, HTTPException
from auth import RoleEnum, get_current_user

from core.user_model import UserBase

router = APIRouter()


@router.get("/info/")
async def get_info(
    current_user: UserBase = Depends(get_current_user()),
):
    """
    Test for info all access
    """
    return current_user


@router.get("/admin-access/")
async def admin_access(
    current_user: UserBase = Depends(get_current_user(required_roles=[RoleEnum.admin])),
):
    """
    Test for admin access
    """
    return current_user


@router.get("/all-except-user/")
async def except_user(
    current_user: UserBase = Depends(
        get_current_user(
            required_roles=[RoleEnum.admin, RoleEnum.manager, RoleEnum.support]
        )
    ),
):
    """
    Test for all except user access
    """
    return current_user
