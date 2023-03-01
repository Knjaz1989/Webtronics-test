from aioredis.client import Redis
from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_async import get_async_session
from . import db_handlers as db_h
from apps.main_utils import get_redis, get_hash_token
from .schemas import UserCreate, UserLogin
from .utils import create_token, get_hash_password, validate_password
from ..main_dependencies import get_user


async def sign_up(
        user: UserCreate,
        session: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    db_user = await db_h.get_user_by_email(session, user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Email already registered.')
    hash_password = get_hash_password(user.password)
    await db_h.create_user(session, user.name, hash_password, user.email)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={'detail': 'The user was created successfully'}
    )


async def login(
        user: UserLogin,
        session=Depends(get_async_session),
        redis: Redis = Depends(get_redis)
) -> dict:
    db_user = await db_h.get_user_by_email(session, user.email)
    if not db_user or \
            not validate_password(
                user.password, db_user.hashed_password
            ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user.password = get_hash_password(user.password)
    access_token, expires = create_token(data=user.dict())
    await redis.set(
        name=user.email,
        value=get_hash_token(access_token),
        ex=user.expire_seconds
    )
    return {"access_token": access_token, "expires": expires}


async def delete_user(
        user=Depends(get_user),
        session: AsyncSession = Depends(get_async_session),
        redis: Redis = Depends(get_redis)
) -> dict:
    await redis.delete(user.email)
    await db_h.delete_user(session, user.id)
    return {'detail': 'User was deleted successfully'}
