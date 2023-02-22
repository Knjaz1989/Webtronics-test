from fastapi import HTTPException, status

from apps.posts import db_handlers as db_h


async def set_rate(user_id: int, post_id: int, action: str):
    is_owner = await db_h.check_owner(user_id, post_id)
    if is_owner:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can't rate your own post",
        )
    rate = await db_h.get_rate(user_id, post_id)
    if not rate:
        await db_h.create_rate(user_id, post_id, action)
    if rate[action] is True:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"You already {action}d the post",
        )
    await db_h.update_rate(user_id, post_id, action)
