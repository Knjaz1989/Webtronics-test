from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, \
    async_sessionmaker

from settings import config


engine = create_async_engine(config.ASYNC_SQLALCHEMY_URL, echo=True)


async_session = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session
        await session.commit()
