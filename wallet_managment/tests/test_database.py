# TODO
import uuid
import pytest
import httpx
from app.main import app

@pytest.mark.asyncio
async def test_create_wallet_success():
    wallet_uuid = str(uuid.uuid4())
    async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.post("/api/v1/wallets", json={"uuid": wallet_uuid, "balance": 100.50, "version": 1})
        assert response.status_code == 200
        assert response.json() == {"balance": 100.50, "version": 1}

@pytest.mark.asyncio
async def test_create_wallet_negative_balance():
    async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.post("/api/v1/wallets", json={"uuid": "123e4567-e89b-12d3-a456-426614174003", "balance": -100})
        assert response.status_code == 400
        assert response.json() == {"detail": "Initial balance cannot be negative.", "code": 400}

@pytest.mark.asyncio
async def test_create_wallet_existing_uuid():
    wallet_uuid = "123e4567-e89b-12d3-a456-426614174000"
    async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
        # Сначала создаем кошелек с этим UUID
        await client.post("/api/v1/wallets", json={"uuid": wallet_uuid, "balance": 100, "version": 1})

        # Затем пытаемся создать кошелек с тем же UUID
        response = await client.post("/api/v1/wallets", json={"uuid": wallet_uuid, "balance": 100})
        assert response.status_code == 400
        assert response.json() == {"detail": "Wallet with this UUID already exists.", "code": 400}
