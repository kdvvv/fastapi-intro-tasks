import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_reverse_text():
    response = client.get("/reverse/hello")
    assert response.status_code == 200
    assert response.json() == {"reversed": "olleh"}

def test_reverse_text_with_spaces():
    response = client.get("/reverse/hello world")
    assert response.status_code == 200
    assert response.json() == {"reversed": "dlrow olleh"}

def test_reverse_text_empty_string():
    response = client.get("/reverse/")
    assert response.status_code == 404  # FastAPI автоматически обработает отсутствие текста в URL
