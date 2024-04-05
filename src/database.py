from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from config import settings

engine = AsyncEngine(create_engine(settings.DATABASE_URL, echo=True, future=True))


async def get_session() -> AsyncSession:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)  # NOQA typing
    async with async_session() as session:
        yield session
