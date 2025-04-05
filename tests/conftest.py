"""
Wrap all async sqlalchemy code into sync code
"""

import asyncio
from typing import AsyncIterator
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.session import (
    get_db,
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
    Base,
)
from app.config import Settings

settings = Settings(
    database_url="sqlite+aiosqlite:///:memory:",
    database_connection_args={"check_same_thread": False},
)


engine = create_async_engine(
    settings.database_url,
    echo=settings.database_echo,
    future=True,
    connect_args=settings.database_connection_args,
)
TestingAsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def get_db_testing() -> AsyncIterator[AsyncSession]:
    """
    Async generator that yields database sessions.
    """
    async with TestingAsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def setup_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def clear_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def get_one_session():
    async for session in get_db_testing():
        return session


@pytest.fixture()
def test_db():
    asyncio.run(setup_db())

    session = asyncio.run(get_one_session())
    try:
        yield session
    finally:
        asyncio.run(session.close())
        asyncio.run(clear_db())


@pytest.fixture()
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            asyncio.run(test_db.close())

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(test_db):
    from app.schemas.user import UserCreate
    from app.services.user_service import create_user

    # noinspection PyTypeChecker
    user = UserCreate(email="test@example.com", password="testpass")
    return asyncio.run(create_user(test_db, user=user))


@pytest.fixture
def test_token(test_user):
    from app.utils.security import create_access_token

    return create_access_token(data={"sub": test_user.email})
