from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from apps.site.utils import helpers as hls
from apps.site.schemas.post_schemas import PostAdd, PostDelete, PostUpdate


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def add_post(post: PostAdd, token: str = Depends(oauth2_scheme)):
    data = hls.decode_token(token)
    db_user = await hls.get_user_by_email(data.get("email"))
    await hls.create_post(user_id=db_user.get("id"), data=post.dict())
    return {"status": "Success", "msg": "The post was created successfully"}


async def get_all_posts(token: str = Depends(oauth2_scheme)):
    hls.decode_token(token)
    posts = await hls.get_posts()
    return {"status": "Success", "data": posts}


async def delete_post(post_data: PostDelete,
                      token: str = Depends(oauth2_scheme)):
    data = hls.decode_token(token)
    db_user = await hls.get_user_by_email(data.get("email"))
    await hls.delete_post(db_user.get("id"), post_data.post_id)
    return {"status": "Success", "msg": 'The post was deleted successfully'}


async def change_post(post_data: PostUpdate, token: str = Depends(oauth2_scheme)):
    """Update post in the database"""
    data = hls.decode_token(token)
    db_user = await hls.get_user_by_email(data.get("email"))
    await hls.change_post(db_user.get("id"), post_data.dict())
    return {"status": "Success", "msg": 'The post was changed successfully'}
