from redis.asyncio import Redis
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from auth import RoleEnum, TokenType, Token
from config import settings
from core.user_model import UserBase, UserCreate
from .schema import LoginPayload, CreateAccountPayload
from auth.token import get_valid_tokens, add_token_to_redis
from db import get_redis_client, get_mongo_database, AgnosticDatabase
from auth.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
)

router = APIRouter()


@router.post("/login/")
async def login(
    data: LoginPayload = Body(...),
    mongo_client: AgnosticDatabase = Depends(get_mongo_database),
    redis_client: Redis = Depends(get_redis_client),
):
    """
    Login for all users
    TODO: Add OTP / Add verify email / Add recaptcha / Add two step verify / Add policy too many login / Add policy brute force
    """

    user = await mongo_client.users.find_one({"username": data.username})

    if not user:
        raise HTTPException(status_code=401, detail="Username or Password incorrect")
    if not verify_password(data.password, user["hashed_password"]):
        return HTTPException(status_code=401, detail="Username or Password incorrect")

    data_jwt = UserBase(
        user_id=str(user["_id"]),
        username=data.username,
        role=RoleEnum(user["role"]),
    )

    access_token = create_access_token(data_jwt)
    refresh_token = create_refresh_token(data_jwt)

    valid_access_tokens = await get_valid_tokens(
        redis_client, str(user["_id"]), TokenType.ACCESS
    )
    if valid_access_tokens:
        await add_token_to_redis(
            redis_client,
            str(user["_id"]),
            access_token,
            TokenType.ACCESS,
            settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )
    valid_refresh_tokens = await get_valid_tokens(
        redis_client, str(user["_id"]), TokenType.REFRESH
    )
    if valid_refresh_tokens:
        await add_token_to_redis(
            redis_client,
            str(user["_id"]),
            refresh_token,
            TokenType.REFRESH,
            settings.REFRESH_TOKEN_EXPIRE_MINUTES,
        )

    response = Token(
        access_token=access_token,
        token_type="bearer",
        refresh_token=refresh_token,
        user_id=str(user["_id"]),
    )

    return response


@router.post("/login-docs/")
async def login(
    data: OAuth2PasswordRequestForm = Depends(),
    mongo_client: AgnosticDatabase = Depends(get_mongo_database),
    redis_client: Redis = Depends(get_redis_client),
):
    """
    Login for all users
    TODO: Add OTP / Add verify email / Add recaptcha / Add two step verify / Add policy too many login / Add policy brute force
    """

    user = await mongo_client.users.find_one({"username": data.username})

    if not user:
        raise HTTPException(status_code=401, detail="Username or Password incorrect")
    if not verify_password(data.password, user["hashed_password"]):
        return HTTPException(status_code=401, detail="Username or Password incorrect")

    data_jwt = UserBase(
        user_id=str(user["_id"]),
        username=data.username,
        role=RoleEnum(user["role"]),
    )

    access_token = create_access_token(data_jwt)
    refresh_token = create_refresh_token(data_jwt)

    valid_access_tokens = await get_valid_tokens(
        redis_client, str(user["_id"]), TokenType.ACCESS
    )
    if valid_access_tokens:
        await add_token_to_redis(
            redis_client,
            str(user["_id"]),
            access_token,
            TokenType.ACCESS,
            settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )
    valid_refresh_tokens = await get_valid_tokens(
        redis_client, str(user["_id"]), TokenType.REFRESH
    )
    if valid_refresh_tokens:
        await add_token_to_redis(
            redis_client,
            str(user["_id"]),
            refresh_token,
            TokenType.REFRESH,
            settings.REFRESH_TOKEN_EXPIRE_MINUTES,
        )

    response = Token(
        access_token=access_token,
        token_type="bearer",
        refresh_token=refresh_token,
        user_id=str(user["_id"]),
    )

    return response


@router.post("/create/", response_model=Token)
async def create_user(
    data: CreateAccountPayload = Body(...),
    mongo_client: AgnosticDatabase = Depends(get_mongo_database),
    redis_client: Redis = Depends(get_redis_client),
):
    """
    Create account sample code


    roles:

        - user

        - support

        - manager

        - admin


    TODO: Add strong password / Add login with google / Add login with facebook
    """
    if await mongo_client.users.find_one({"username": data.username}):
        raise HTTPException(status_code=400, detail="Username already exists")

    user = UserCreate(
        username=data.username,
        hashed_password=get_password_hash(data.password),
        role=data.role,
    )

    user = await mongo_client.users.insert_one(user.dict())
    user_id = str(user.inserted_id)

    data_jwt = UserBase(
        user_id=str(user["_id"]),
        username=data.username,
        role=RoleEnum(user["role"]),
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
    )

    return response
