import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/users", json={"username": "testuser", "email": "testuser@example.com"})
    assert response.status_code == 200
    assert response.json() == {"username": "testuser", "email": "testuser@example.com", "age": None, "status": "User created"}

def test_create_user_with_age():
    response = client.post("/users", json={"username": "testuser", "email": "testuser@example.com", "age": 25})
    assert response.status_code == 200
    assert response.json() == {"username": "testuser", "email": "testuser@example.com", "age": 25, "status": "User created"}

def test_create_user_missing_email():
    response = client.post("/users", json={"username": "testuser"})
    assert response.status_code == 422  # Ошибка 422, если отсутствует обязательный параметр email
