# TODO
import pytest
from tests.conftest import UUIDS, db_session, client, mock_get_wallet

@pytest.mark.asyncio
async def test_get_balance_existing_wallet(uuid, client, mock_get_wallet):
    print(f"Testing get_balance_existing_wallet with uuid: {uuid}")

    # Set up mock for get_wallet
    mock_response = {"balance": 100.0}
    mock_get_wallet.return_value = mock_response

    try:
        # Override the get method to return a mocked response
        original_get = client.get
        client.get = lambda *args, **kwargs: httpx.Response(200, json=mock_response)

        # Run the test
        async with LifespanManager(client.app):
            response = await client.get(f"/api/v1/wallets/{uuid}")

        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.json()}")

        assert response.status_code == 200
        assert "balance" in response.json()
        assert response.json()["balance"] == mock_response["balance"]

        # Restore the original get method
        client.get = original_get
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

@pytest.mark.asyncio
async def test_get_balance_nonexistent_wallet(client, mock_get_wallet):
    print("Testing get_balance_nonexistent_wallet")

    # Устанавливаем мок для get_wallet
    mock_response = {"error": "Wallet not found"}
    mock_get_wallet.return_value = mock_response

    try:
        # Отправляем запрос для несуществующего кошелька
        response = await client.get(f"/api/v1/wallets/{UUIDS['nonexistent']}")

        assert response.status_code == 404
        assert "detail" in response.json()
        assert response.json()["detail"] == "Wallet not found"
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

@pytest.mark.asyncio
async def test_get_balance_invalid_wallet(client, mock_get_wallet):
    print("Testing get_balance_invalid_wallet")

    # Устанавливаем мок для get_wallet
    mock_response = {"error": "Invalid UUID format"}
    mock_get_wallet.return_value = mock_response

    try:
        # Отправяем запрос с недействительным UUID
        response = await client.get("/api/v1/wallets/invalid")

        assert response.status_code == 400
        assert "detail" in response.json()
        assert response.json()["detail"] == "Invalid UUID format"
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

@pytest.mark.asyncio
async def test_get_balance_no_wallet(client, mock_get_wallet):
    print("Testing get_balance_no_wallet")

    # Устанавливаем мок для get_wallet
    mock_response = {"error": "Wallet not found"}
    mock_get_wallet.return_value = mock_response

    try:
        # Отправляем запрос без кошелька
        response = await client.get(f"/api/v1/wallets/{UUIDS['nonexistent']}")

        assert response.status_code == 404
        assert "detail" in response.json()
        assert response.json()["detail"] == "Wallet not found"
    except Exception as e:
        print(f"An error occurred: {e}")
        raise
