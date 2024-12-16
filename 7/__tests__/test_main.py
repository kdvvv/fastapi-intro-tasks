import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

# Фикстура для сброса базы данных перед каждым тестом
@pytest.fixture(autouse=True)
def reset_product_list():
    # Очищаем список продуктов перед каждым тестом
    from src.main import product_list
    product_list.clear()

def test_create_product():
    response = client.post("/product", json={"name": "Product A", "price": 19.99, "quantity": 100})
    assert response.status_code == 200
    assert response.json()["message"] == "Product added successfully"
    assert response.json()["product"]["name"] == "Product A"
    assert response.json()["product"]["price"] == 19.99
    assert response.json()["product"]["quantity"] == 100

def test_create_product_invalid_price():
    response = client.post("/product", json={"name": "Product B", "price": -10.0, "quantity": 100})
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "ensure this value is greater than 0"

def test_create_product_invalid_quantity():
    response = client.post("/product", json={"name": "Product C", "price": 20.0, "quantity": -5})
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "ensure this value is greater than or equal to 0"

def test_get_products():
    client.post("/product", json={"name": "Product A", "price": 19.99, "quantity": 100})
    response = client.get("/products")
    assert response.status_code == 200
    assert len(response.json()["products"]) == 1
    assert response.json()["products"][0]["name"] == "Product A"
    assert response.json()["products"][0]["price"] == 19.99
    assert response.json()["products"][0]["quantity"] == 100

def test_create_multiple_products():
    client.post("/product", json={"name": "Product A", "price": 19.99, "quantity": 100})
    client.post("/product", json={"name": "Product B", "price": 29.99, "quantity": 50})
    response = client.get("/products")
    assert len(response.json()["products"]) == 2
    assert response.json()["products"][0]["name"] == "Product A"
    assert response.json()["products"][1]["name"] == "Product B"
