import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_login():
    form_data = {"username": "testuser", "password": "securepassword"}
    response = client.post("/login", data=form_data)
    assert response.status_code == 200
    assert response.json() == {
        "username": "testuser",
        "password": "securepassword",
        "status": "Login successful"
    }

def test_login_missing_password():
    form_data = {"username": "testuser"}
    response = client.post("/login", data=form_data)
    assert response.status_code == 422  # Ошибка 422, если отсутствует обязательный параметр password

def test_login_missing_username():
    form_data = {"password": "securepassword"}
    response = client.post("/login", data=form_data)
    assert response.status_code == 422  # Ошибка 422, если отсутствует обязательный параметр username
