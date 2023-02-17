from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from . import helpers as hls


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_user(token: str = Depends(oauth2_scheme)):
    user = hls.decode_token(token)
    db_user = await hls.get_user_by_email(user.get("email"))
    return db_user
