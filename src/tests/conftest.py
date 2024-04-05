import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from database import get_session
from main import app


@pytest_asyncio.fixture()
async def async_session():
    # TODO: better using a prod DB (for example postgres)
    async_engine: AsyncEngine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True, future=True)
    # init all tables
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with AsyncSession(async_engine) as session:

        async def override_get_db():
            return session

        # patching of dependencies and throw session
        app.dependency_overrides[get_session] = override_get_db
        yield session
        app.dependency_overrides.clear()


@pytest_asyncio.fixture()
async def api_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
