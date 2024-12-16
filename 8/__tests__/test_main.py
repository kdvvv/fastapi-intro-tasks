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
    response = client.post("/product", json={
        "name": "T-Shirt",
        "price": 29.99,
        "specifications": {
            "size": "M",
            "color": "Red",
            "material": "Cotton"
        }
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Product added successfully"
    assert response.json()["product"]["name"] == "T-Shirt"
    assert response.json()["product"]["price"] == 29.99
    assert response.json()["product"]["specifications"]["size"] == "M"
    assert response.json()["product"]["specifications"]["color"] == "Red"
    assert response.json()["product"]["specifications"]["material"] == "Cotton"

def test_create_product_invalid_price():
    response = client.post("/product", json={
        "name": "T-Shirt",
        "price": -10.0,
        "specifications": {
            "size": "M",
            "color": "Red",
            "material": "Cotton"
        }
    })
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "ensure this value is greater than 0"

def test_create_product_missing_specifications():
    response = client.post("/product", json={
        "name": "T-Shirt",
        "price": 29.99
    })
    assert response.status_code == 422
    assert "specifications" in response.json()["detail"][0]["loc"]

def test_get_products():
    client.post("/product", json={
        "name": "T-Shirt",
        "price": 29.99,
        "specifications": {
            "size": "M",
            "color": "Red",
            "material": "Cotton"
        }
    })
    response = client.get("/products")
    assert response.status_code == 200
    assert len(response.json()["products"]) == 1
    assert response.json()["products"][0]["name"] == "T-Shirt"
    assert response.json()["products"][0]["price"] == 29.99
    assert response.json()["products"][0]["specifications"]["size"] == "M"
    assert response.json()["products"][0]["specifications"]["color"] == "Red"
    assert response.json()["products"][0]["specifications"]["material"] == "Cotton"

def test_create_multiple_products():
    client.post("/product", json={
        "name": "T-Shirt",
        "price": 29.99,
        "specifications": {
            "size": "M",
            "color": "Red",
            "material": "Cotton"
        }
    })
    client.post("/product", json={
        "name": "Jeans",
        "price": 49.99,
        "specifications": {
            "size": "L",
            "color": "Blue",
            "material": "Denim"
        }
    })
    response = client.get("/products")
    assert len(response.json()["products"]) == 2
    assert response.json()["products"][0]["name"] == "T-Shirt"
    assert response.json()["products"][1]["name"] == "Jeans"
