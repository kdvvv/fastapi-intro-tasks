import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_get_user_valid_id():
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json() == {"user_id": 1}

def test_get_user_invalid_id():
    response = client.get("/users/0")
    assert response.status_code == 422

def test_get_user_negative_id():
    response = client.get("/users/-5")
    assert response.status_code == 422
