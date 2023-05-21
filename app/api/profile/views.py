from bson import ObjectId
from fastapi import APIRouter, Body, Depends, HTTPException
from auth import get_current_user
from db import get_mongo_database, AgnosticDatabase
from core.user_model import UserBase
from .schema import Profile


router = APIRouter()


@router.get("/", response_model=Profile)
async def get_info(
    current_user: UserBase = Depends(get_current_user()),
    mongo_client: AgnosticDatabase = Depends(get_mongo_database),
):
    """
    Get info current user
    """

    data = await mongo_client.users.find_one({"_id": ObjectId(current_user.user_id)})
    del data["_id"]

    return data


@router.put("/", response_model=Profile)
async def update_info(
    payload: Profile,
    current_user: UserBase = Depends(get_current_user()),
    mongo_client: AgnosticDatabase = Depends(get_mongo_database),
):
    """
    Get info current user
    """

    await mongo_client.users.update_one(
        {"_id": ObjectId(current_user.user_id)}, {"$set": payload.dict()}
    )

    data = await mongo_client.users.find_one({"_id": ObjectId(current_user.user_id)})
    del data["_id"]

    return data
