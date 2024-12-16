import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_filter_default_values():
    response = client.get("/filter")
    assert response.status_code == 200
    assert response.json() == {"min": 0, "max": 100}

def test_filter_custom_values():
    response = client.get("/filter?min=10&max=50")
    assert response.status_code == 200
    assert response.json() == {"min": 10, "max": 50}

def test_filter_min_out_of_bounds():
    response = client.get("/filter?min=-1")
    assert response.status_code == 422

def test_filter_max_out_of_bounds():
    response = client.get("/filter?max=101")
    assert response.status_code == 422
