from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from redis.asyncio import Redis
from jose import jwt, JWTError
from pydantic import ValidationError

from config import settings
from core.user_model import User
from db.redis import get_redis_client
from auth.token import get_valid_tokens
from core.common_schema import TokenType

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login-docs/")


def get_current_user(required_roles: list[str] = None) -> User:
    async def current_user(
        token: str = Depends(reusable_oauth2),
        redis_client: Redis = Depends(get_redis_client),
    ) -> User:
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
        except (JWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
            )
        user_id = payload["user_id"]
        valid_access_tokens = await get_valid_tokens(
            redis_client, user_id, TokenType.ACCESS
        )
        if valid_access_tokens and token not in valid_access_tokens:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
            )
        # user: User = await crud.user.get(id=user_id)
        # if not user:
        #     raise HTTPException(status_code=404, detail="User not found")

        # if not user.is_active:
        #     raise HTTPException(status_code=400, detail="Inactive user")

        if required_roles:
            is_valid_role = False
            for role in required_roles:
                if role == payload["role"]:
                    is_valid_role = True

            if not is_valid_role:
                raise HTTPException(
                    status_code=403,
                    # detail=f"""Role "{required_roles}" is required for this action""",
                    detail=f"""Access denied!""",
                )

        return payload

    return current_user
