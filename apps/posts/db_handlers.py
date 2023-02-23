from sqlalchemy import insert, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Post, Rates


async def create_post(
        session: AsyncSession,user_id: int, title: str, content: str,
) -> None:
    """Add post into the database"""
    stmt = insert(Post).values(title=title, content=content, user_id=user_id)
    await session.execute(stmt)


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
    ).returning(Post.id)
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


async def get_post(post_id: int) -> dict | None:
    """Get current post from the database"""
    query = """
        SELECT * FROM posts WHERE id = :id;
        """
    post = db.fetch_one(query=query, values={'id': post_id})
    if post:
        return dict(post._mapping)


async def get_posts():
    """Get all posts from the database"""
    query = """
        SELECT * FROM posts;
        """
    posts = await db.fetch_all(query=query)
    return posts


async def get_ids_of_all_users_posts(user_id: int):
    pass


async def search_posts(title: str = None, content: str = None):
    """Search posts from the database"""
    select_list = []
    values = {'title': title, 'content': content}
    new_values = {}
    for key, value in values.items():
        if value:
            select_list.append(
                f"STRING_TO_ARRAY(LOWER({key}), ' ') && ARRAY[:{key}]"
            )
            new_values[key] = value
    query = f"""
        SELECT id, title, content FROM posts WHERE {' AND '.join(select_list)}; 
        """
    posts = await db.fetch_all(query=query, values=new_values)
    return posts


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
    query = """
        DELETE FROM rates 
        WHERE user_id = :user_id AND post_id = :post_id 
        RETURNING *
        """
    stmt = delete(Rates).where(
        Rates.user_id == user_id, Rates.post_id == post_id
    )
    rate = await session.execute(stmt)
    if not rate:
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
