import os
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models.org import Base
from app.main import app
from app.core.database import get_db

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://test_user:test_pass@localhost:5432/test_db",
)


@pytest.fixture(scope="session")
async def engine():
    """Создаёт тестовый движок и таблицы один раз за всю сессию."""
    test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield test_engine
    await test_engine.dispose()


@pytest.fixture
async def db_session(engine):
    """Для каждого теста: новое соединение, транзакция, сессия."""
    connection = await engine.connect()
    trans = await connection.begin()
    async_session = sessionmaker(
        connection, class_=AsyncSession, expire_on_commit=False
    )
    session = async_session()

    async def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db

    yield session

    await session.close()
    await trans.rollback()
    await connection.close()
    app.dependency_overrides.pop(get_db, None)


@pytest.fixture
async def client(db_session):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
