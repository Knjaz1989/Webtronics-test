from fastapi import Depends

from apps.site.utils import helpers as hls, db_handlers as db_h
from apps.site.schemas.post_schemas import PostBase, PostAdd, PostUpdate, \
    PostRate, PostSearch
from apps.site.utils.dependencies import get_user


async def add_post(post: PostAdd, user: dict = Depends(get_user)):
    await db_h.create_post(user.get("id"), post.title, post.content)
    return {"status": "Success", "msg": "The post was created successfully"}


async def get_all_posts(user: dict = Depends(get_user)):
    posts = await db_h.get_posts()
    return {"status": "Success", "data": posts}


async def delete_post(post_data: PostBase, user: dict = Depends(get_user)):
    await db_h.delete_post(user.get("id"), post_data.id)
    return {"status": "Success", "msg": 'The post was deleted successfully'}


async def change_post(
        post_data: PostUpdate, user: dict = Depends(get_user)
):
    await db_h.change_post(user.get("id"), post_data.title, post_data.content)
    return {"status": "Success", "msg": 'The post was changed successfully'}


async def rate_post(post: PostRate, user: dict = Depends(get_user)):
    await hls.set_rate(
        user_id=user.get("id"), post_id=post.id, rate=post.action.value
    )
    return {"status": "Success",
            "msg": f'You paste {post.action.value} successfully'}


async def unrate_post(post_data: PostBase, user: dict = Depends(get_user)):
    await hls.delete_rate(user.get('id'), post_data.id)
    return {"status": "Success", "msg": 'The rate was deleted successfully'}


async def search_post(post_data: PostSearch, user: dict = Depends(get_user)):
    posts = await db_h.search_posts(post_data.title, post_data.content)
    return {'status': 'Success', 'data': posts}
