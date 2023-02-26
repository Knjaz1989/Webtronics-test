from sqlalchemy import insert, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from apps.main_helpers import model_to_dict, models_to_dict
from database.models import Post, Rates
from settings import config


async def create_post(
        session: AsyncSession, user_id: int, title: str, content: str,
) -> None:
    """Add post into the database"""
    stmt = insert(Post).\
        values(title=title, content=content, user_id=user_id).\
        returning(Post)
    post = await session.execute(stmt)
    post = post.scalars().first()
    return model_to_dict(post)


async def get_own_post(
        session: AsyncSession, user_id: int, post_id: int):
    stmt = select(Post).where(Post.id == post_id, Post.user_id == user_id)
    post = await session.execute(stmt)
    post = post.scalars().first()
    if post:
        return post


async def delete_post(
        session: AsyncSession, user_id: int, post_id: int
):
    """Delete post from the database"""
    stmt = delete(Post).where(
        Post.id == post_id, Post.user_id == user_id
    ).returning(Post)
    post = await session.execute(stmt)
    post = post.scalars().first()
    if post:
        return post


async def change_post(session: AsyncSession, user_id: int, post_data: dict):
    """Change current post in the database"""
    post_id = post_data.pop('id')
    post_data = {key: value for key, value in post_data.items() if value}
    stmt = update(Post).where(
        Post.id == post_id, Post.user_id == user_id
    ).values(**post_data)
    await session.execute(stmt)


async def get_post(session: AsyncSession, post_id: int):
    """Get current post from the database"""
    stmt = select(Post).where(Post.id == post_id)
    post = await session.execute(stmt)
    post = post.scalars().first()
    if post:
        return model_to_dict(post)


async def get_posts(
        session: AsyncSession, page: int, limit: int = config.POSTS_LIMIT):
    """Get all posts from the database"""
    stmt = select(Post).offset(page * limit - limit).limit(limit)
    posts = await session.execute(stmt)
    posts = posts.scalars().all()
    posts = models_to_dict(posts)
    return posts


async def search_posts(
        session: AsyncSession, page: int, limit: int = config.POSTS_LIMIT,
        title: str = None, content: str = None,
):
    """Search posts from the database"""
    if not title:
        title = '%'
    else:
        title = '%' + title + '%'
    if not content:
        content = '%'
    else:
        content = '%' + content + '%'
    stmt = select(Post).\
        where(Post.title.ilike(title), Post.content.ilike(content)).\
        offset(page * limit - limit).limit(limit)
    posts = await session.execute(stmt)
    posts = posts.scalars().all()
    return models_to_dict(posts)


async def create_rate(
        session: AsyncSession, user_id: int, post_id: int, rate: str
):
    values = {'like': False, 'dislike': False}
    values[rate] = True
    stmt = insert(Rates).values(
        user_id=user_id, post_id=post_id, **values
    )
    await session.execute(stmt)


async def delete_rate(session: AsyncSession, user_id: int, post_id: int):
    stmt = delete(Rates).where(
        Rates.user_id == user_id, Rates.post_id == post_id
    ).returning(Rates)
    rate = await session.execute(stmt)
    rate = rate.scalars().first()
    if rate:
        return rate


async def get_own_rate(
        session: AsyncSession, user_id: int, post_id: int
):
    stmt = select(Rates).where(
        Rates.user_id == user_id, Rates.post_id == post_id
    )
    rate = await session.execute(stmt)
    rate = rate.scalars().first()
    if rate:
        return rate


async def update_rate(
        session: AsyncSession, user_id: int, post_id: int, action: str
):
    values = {'like': False, 'dislike': False}
    if action == 'like':
        values['like'] = True
    else:
        values['dislike'] = True
    stmt = update(Rates). \
        where(Rates.post_id == post_id, Rates.user_id == user_id).\
        values(**values)
    await session.execute(stmt)
