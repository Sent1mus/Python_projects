# TODO
from fastapi.testclient import TestClient
from app.main import app  # Импортируем app из main.py

client = TestClient(app)

def test_http_exception_handler():
    response = client.get("/api/v1/wallets/invalid-uuid")
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid UUID format", "code": 400}

def test_validation_exception_handler():
    response = client.post("/api/v1/wallets/123e4567-e89b-12d3-a456-426614174000/operation", json={"amount": 0})
    assert response.status_code == 422
    assert response.json() == {"detail": "Validation Error", "code": 422}
