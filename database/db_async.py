from databases import Database
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from settings import config


DATABASE_URL = config.ASYNC_SQLALCHEMY_URL

db = Database(DATABASE_URL, force_rollback=False)


# engine = create_async_engine(
#     config.ASYNC_SQLALCHEMY_URL,
#     echo=True,
#     future=True,
# )
# async_session = sessionmaker(
#     engine, class_=AsyncSession, expire_on_commit=False
# )
# db = async_session
#
# async def get_session() -> AsyncSession:
#     async with async_session() as session:
#         yield session
