from sqlalchemy import select, insert, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User


async def create_user(
    session: AsyncSession, user_name: str, hashed_password: str, email: str
) -> None:
    """Add user into the database"""
    stmt = insert(User).values(
        name=user_name, hashed_password=hashed_password, email=email
    )
    await session.execute(stmt)


async def delete_user(session: AsyncSession, user_id: int) -> None:
    """Delete user from the database"""
    stmt = delete(User).where(and_(User.id == user_id))
    await session.execute(stmt)


async def get_user_by_email(session: AsyncSession, email: str):
    """Get user from the database by email"""
    stmt = select(User).where(and_(User.email == email))
    print(stmt)
    user_db = await session.execute(stmt)
    user_db = user_db.scalars().first()
    if user_db:
        return user_db
