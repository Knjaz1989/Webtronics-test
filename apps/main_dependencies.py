from aioredis.client import Redis
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from .main_utils import get_redis, get_hash_token
from database.db_async import get_async_session
from apps.auth import db_handlers as db_h
from apps.posts.utils import decode_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_user(
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(get_async_session),
        redis: Redis = Depends(get_redis)
):
    user = decode_token(token)
    hash = await redis.get(user.get('email'))
    if not hash or hash != get_hash_token(token):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Your token has been expired",
        )
    db_user = await db_h.get_user_by_email(session, user.get("email"))
    if db_user:
        return db_user
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="There is no such user with this token",
    )
