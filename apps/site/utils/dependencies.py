from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from . import helpers as hls, db_handlers as db_h, jwt_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_user(token: str = Depends(oauth2_scheme)):
    user = jwt_token.decode_token(token)
    db_user = db_h.get_user_by_email(user.get("email"))
    return db_user
