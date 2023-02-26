import asyncio

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession,\
    async_sessionmaker
import pytest

from apps.server import app
from database.db_async import get_async_session
from database.models import Base
from settings import config


engine_test = create_async_engine(config.TEST_ASYNC_SQLALCHEMY_URL)

async_test_session = async_sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)


async def get_test_async_session() -> AsyncSession:
    async with async_test_session() as session:
        yield session
        await session.commit()

# Override the main session on the test session
app.dependency_overrides[get_async_session] = get_test_async_session


@pytest.fixture(autouse=True, scope='class')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
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


@pytest.fixture(scope='class')
async def main_token(async_client):
    response_1 = await async_client.post(
        "/user/sign-up",
        json={
            'name': 'Igor', 'email': 'knjaz1989@gmail.com',
            'password': '12345678'
        }
    )
    response_2 = await async_client.post(
        "/user/login",
        json={'email': 'knjaz1989@gmail.com', 'password': '12345678'}
    )
    token = response_2.json().get('access_token')
    return token


@pytest.fixture(scope='class')
async def second_token(async_client):
    response_1 = await async_client.post(
        "/user/sign-up",
        json={
            'name': 'Vasya', 'email': 'knjaz1989@yandex.com',
            'password': '12345678'
        }
    )
    response_2 = await async_client.post(
        "/user/login",
        json={'email': 'knjaz1989@yandex.com', 'password': '12345678'}
    )
    token = response_2.json().get('access_token')
    return token
