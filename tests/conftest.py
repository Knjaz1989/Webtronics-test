from httpx import AsyncClient
import pytest_asyncio

from apps.server import app, startup, shutdown


@pytest_asyncio.fixture
async def app_client():
    await startup()
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client
    await shutdown()
