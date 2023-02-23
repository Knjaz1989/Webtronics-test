from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from apps.posts import db_handlers as db_h


async def is_post_owner(
        session: AsyncSession, user_id: int, post_id: int
):
    post = await db_h.get_own_post(session, user_id, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This is not your post",
        )


async def is_not_post_owner(
        session: AsyncSession, user_id: int, post_id: int
):
    post = await db_h.get_own_post(session, user_id, post_id)
    if post:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This is your post",
        )


async def is_rate_owner(
        session: AsyncSession, user_id: int, post_id: int
):
    rate = await db_h.get_own_rate(session, user_id, post_id)
    if not rate:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This is not your rate",
        )


async def set_rate(
        session: AsyncSession, user_id: int, post_id: int, action: str
):
    rate = await db_h.get_own_rate(session, user_id, post_id)
    if not rate:
        await db_h.create_rate(session, user_id, post_id, action)
        return
    if rate.__dict__[action] is True:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"You already {action}d the post",
        )
    await db_h.update_rate(session, user_id, post_id, action)
