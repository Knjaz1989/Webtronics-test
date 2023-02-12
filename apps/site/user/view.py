from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from apps.site.utils import user_helpers
from apps.site.schemas.users import UserCreate, UserLogin

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login",
)


async def sign_up(user: UserCreate):
    db_user = await user_helpers.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Email already registered.')
    return await user_helpers.create_user(user=user)


async def login(data: UserLogin):
    db_user = await user_helpers.get_user_by_email(data.email)
    if not db_user or \
            not user_helpers.validate_password(
                data.password, db_user.hashed_password
            ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": 'тут буде токен', "token_type": "bearer"}
