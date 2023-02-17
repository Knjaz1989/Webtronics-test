from fastapi import Depends

from apps.site.utils import helpers as hls
from apps.site.schemas.post_schemas import PostAdd, PostDelete, PostUpdate, \
    PostBase
from apps.site.utils.dependencies import get_user


async def add_post(post: PostAdd, user: dict = Depends(get_user)):
    await hls.create_post(user_id=user.get("id"), data=post.dict())
    return {"status": "Success", "msg": "The post was created successfully"}


async def get_all_posts(user: dict = Depends(get_user)):
    posts = await hls.get_posts()
    return {"status": "Success", "data": posts}


async def delete_post(post_data: PostDelete, user: dict = Depends(get_user)):
    await hls.delete_post(user.get("id"), post_data.post_id)
    return {"status": "Success", "msg": 'The post was deleted successfully'}


async def change_post(
        post_data: PostUpdate, user: dict = Depends(get_user)
):
    await hls.change_post(user.get("id"), post_data.dict())
    return {"status": "Success", "msg": 'The post was changed successfully'}


async def paste_like(post: PostBase, user: dict = Depends(get_user)):
    await hls.rate_post(rate_type='like')
    return {"status": "Success", "msg": 'You paste like successfully'}


def paste_dislike():
    return {"status": "Success", "msg": 'You paste dislike successfully'}
