import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_language_cookie_set():
    response = client.get("/language", cookies={"language": "en"})
    assert response.status_code == 200
    assert response.json() == {"language": "en"}

def test_language_cookie_not_set():
    response = client.get("/language")
    assert response.status_code == 200
    assert response.json() == {"message": "Language not set"}
