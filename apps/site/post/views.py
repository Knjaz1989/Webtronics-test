from fastapi import HTTPException, status

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from .helpers import create_post
from .schemas import PostAdd
from ..user.helpers import decode_token, get_user_by_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def add_post(post: PostAdd, token: str = Depends(oauth2_scheme)):
    data = decode_token(token)
    db_user = await get_user_by_email(data.get("email"))

    await create_post(user_id=db_user.get("id"), data=post.dict())
    return {"status": "Success", "msg": "The post was created successfully"}
