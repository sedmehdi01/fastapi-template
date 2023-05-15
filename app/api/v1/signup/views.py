from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi import BackgroundTasks
from redis.asyncio import Redis

from config import settings
from auth.role_schema import RoleEnum
from db import get_mongo_database, AgnosticDatabase, get_redis_client
from core.user_model import UserBase
from .schema import SendEmailCodeSchema, VerifyEmailSchema
from api.v1.signup.email_smtp import (
    send_email_async,
    send_email_background,
    verify_code,
)
from auth.security import (
    get_password_hash,
    create_access_token,
    create_refresh_token,
)
from auth.token import get_valid_tokens, add_token_to_redis
from core.common_schema import TokenType, Token, Response

router = APIRouter()


@router.post("/send-email-code/", response_model=Response)
async def send_sms_code(
    payload: SendEmailCodeSchema = Body(...),
):
    """
    Send email code
    """
    await send_email_async(payload.email, payload.username)
    return {"message": "Code sent"}


@router.post("/send-email-code-background/", response_model=Response)
async def send_email_background_tasks(
    background_tasks: BackgroundTasks,
    payload: SendEmailCodeSchema = Body(...),
    mongo_client: AgnosticDatabase = Depends(get_mongo_database),
):
    """
    Send email code with background_tasks
    """

    if await mongo_client.users.find_one({"email": payload.email}):
        raise HTTPException(status_code=400, detail="Email already exists")

    if await mongo_client.users.find_one({"username": payload.username}):
        raise HTTPException(status_code=400, detail="Username already exists")

    await send_email_background(background_tasks, payload.email, payload.username)
    return {"message": "Code sent"}


@router.post("/verify-email-code/", response_model=Token)
async def verify_email(
    payload: VerifyEmailSchema = Body(...),
    mongo_client: AgnosticDatabase = Depends(get_mongo_database),
    redis_client: Redis = Depends(get_redis_client),
):
    """
    Verify email code and insert account to database
    """
    if not await verify_code(payload.email, payload.username, payload.code):
        raise HTTPException(status_code=400, detail="Invalid code")

    user = await mongo_client.users.insert_one(
        {
            "username": payload.username,
            "hashed_password": get_password_hash(payload.password),
            "email": payload.email,
            "role": RoleEnum.user.value,
        }
    )

    user_id = str(user.inserted_id)

    data_jwt = UserBase(
        user_id=user_id,
        username=payload.username,
        role=RoleEnum.user,
    )

    access_token = create_access_token(data_jwt)
    refresh_token = create_refresh_token(data_jwt)

    valid_access_tokens = await get_valid_tokens(
        redis_client, user_id, TokenType.ACCESS
    )
    if valid_access_tokens:
        await add_token_to_redis(
            redis_client,
            user_id,
            access_token,
            TokenType.ACCESS,
            settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )
    valid_refresh_tokens = await get_valid_tokens(
        redis_client, user_id, TokenType.REFRESH
    )
    if valid_refresh_tokens:
        await add_token_to_redis(
            redis_client,
            user_id,
            refresh_token,
            TokenType.REFRESH,
            settings.REFRESH_TOKEN_EXPIRE_MINUTES,
        )

    response = Token(
        access_token=access_token,
        token_type="bearer",
        refresh_token=refresh_token,
        user_id=user_id,
        message="Create User Successful",
    )

    return response
