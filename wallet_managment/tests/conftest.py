# TODO
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from databases import Database
import os
from unittest.mock import patch

# Константы
DATABASE_URL = "postgresql://postgres:944577@localhost/wallet_management"
BASE_URL = "http://localhost:8000"

# Настройка базы данных
database = Database(DATABASE_URL)

@pytest.fixture(scope="session")
async def setup_database():
    print("Connecting to the database...")
    try:
        if not database.is_connected:
            await database.connect()
        print("Database connected.")
        yield
    except Exception as e:
        print(f"Failed to connect to the database: {e}")
        raise
    finally:
        await database.disconnect()

@pytest.fixture(scope="function")
async def db_session():
    await setup_database()
    yield
    await database.disconnect()

@pytest.fixture(scope="function")
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        yield client

@pytest.fixture(scope="function")
def mock_get_wallet():
    with patch('app.main.get_wallet') as mocked:
        yield mocked

UUIDS = {
    "existing": [
        "21aecc43-dd41-4dd0-88e5-f9b39cf2d241",
        "c9660d73-ad01-4a0c-8242-1358ca34c3fa",
    ],
    "nonexistent": "00000000-0000-0000-0000-000000000000",
    "invalid": "invalid-uuid"
}
