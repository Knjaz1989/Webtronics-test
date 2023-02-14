from fastapi import HTTPException, status

from apps.site.utils import helpers as hls
from apps.site.schemas.user_schemas import UserCreate, UserLogin


async def sign_up(user: UserCreate):
    db_user = await hls.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Email already registered.')
    return await hls.create_user(user=user)


async def login(user: UserLogin):
    db_user = await hls.get_user_by_email(user.email)
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
    access_token, expires = hls.create_token(data=user.dict())
    return {"access_token": access_token, "expires": expires}
