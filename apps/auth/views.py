from fastapi import Response, HTTPException, status

from . import helpers as hls, db_handlers as db_h
from .schemas import UserCreate, UserLogin
from .utils import create_token


async def sign_up(user: UserCreate):
    db_user = await db_h.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Email already registered.')
    hash_password = hls.get_hash_password(user.password)
    await db_h.create_user(user.name, hash_password, user.email)
    return Response(content="The user was created successfully")


async def login(user: UserLogin):
    db_user = await db_h.get_user_by_email(user.email)
    if not db_user or \
            not hls.validate_password(
                user.password, db_user.get("hashed_password")
            ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user.password = hls.get_hash_password(user.password)
    access_token, expires = create_token(data=user.dict())
    return {"access_token": access_token, "expires": expires}
