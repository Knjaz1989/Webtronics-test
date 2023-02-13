from fastapi import HTTPException, status

from .helpers import get_user_by_email, create_user, validate_password, \
    create_token, hash_password
from .schemas import UserCreate, UserLogin


async def sign_up(user: UserCreate):
    db_user = await get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Email already registered.')
    return await create_user(user=user)


async def login(user: UserLogin):
    db_user = await get_user_by_email(user.email)
    if not db_user or \
            not validate_password(
                user.password, db_user.hashed_password
            ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user.password = hash_password(user.password)
    access_token, expires = create_token(data=user.dict())
    return {"access_token": access_token, "expires": expires}
