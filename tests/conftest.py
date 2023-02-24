import asyncio

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession,\
    async_sessionmaker
import pytest, pytest_asyncio

from apps.server import app
from database.db_async import get_async_session
from database.models import Base
from settings import config


test_engine = create_async_engine(config.TEST_ASYNC_SQLALCHEMY_URL, echo=True)

test_async_session = async_sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


async def get_test_async_session() -> AsyncSession:
    async with test_async_session() as session:
        yield session
        await session.commit()

# Override the main session on the test session
app.dependency_overrides[get_async_session] = get_test_async_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True, scope='session')
async def async_client():
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client
