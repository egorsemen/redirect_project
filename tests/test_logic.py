import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.main import app
from app.database import Base, get_db

# 1. Используем асинхронный SQLite для тестов
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

# 2. Асинхронное переопределение базы
async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

# 3. Фикстура для создания таблиц перед тестами
@pytest_asyncio.fixture(autouse=True)
async def init_test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.mark.asyncio
async def test_create_shorten():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/shorten", json={"url": "https://google.com"})
    assert response.status_code == 201
    assert "short_id" in response.json()

@pytest.mark.asyncio
async def test_redirect_and_clicks():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        create_res = await ac.post("/shorten", json={"url": "https://python.org"})
        short_id = create_res.json()["short_id"]
        
        await ac.get(f"/{short_id}")

        stats_res = await ac.get(f"/stats/{short_id}")
        
    assert stats_res.status_code == 200
    assert stats_res.json()["clicks"] == 1

@pytest.mark.asyncio
async def test_not_found():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/nonexistent")
    assert response.status_code == 404