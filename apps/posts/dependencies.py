from fastapi import HTTPException, status

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from ..auth import db_handlers as db_h
from .utils import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_user(token: str = Depends(oauth2_scheme)):
    user = decode_token(token)
    db_user = await db_h.get_user_by_email(user.get("email"))
    if db_user:
        return db_user
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="There is no such user with this token",
    )
