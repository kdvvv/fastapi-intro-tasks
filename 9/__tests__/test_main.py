import pytest
from fastapi.testclient import TestClient
from src.main import app, product_list, product_id_counter

client = TestClient(app)

# Фикстура для сброса базы данных перед каждым тестом
@pytest.fixture(autouse=True)
def reset_product_list():
    product_list.clear()
    global product_id_counter
    product_id_counter = 1

# Фикстура для добавления продукта перед тестом
@pytest.fixture
def add_product():
    product_data = {
        "name": "T-Shirt",
        "price": 29.99,
        "specifications": {
            "size": "M",
            "color": "Red",
            "material": "Cotton"
        }
    }
    response = client.post("/product", json=product_data)
    return response.json()  # Возвращаем данные продукта (включая ID)

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
    assert "id" in response.json()
    assert response.json()["name"] == "T-Shirt"
    assert response.json()["price"] == 29.99
    assert len(product_list) == 1

def test_create_product_invalid_price():
    response = client.post("/product", json={
        "name": "T-Shirt",
        "price": 0,
        "specifications": {
            "size": "M",
            "color": "Red",
            "material": "Cotton"
        }
    })
    assert response.status_code == 422

def test_get_products(add_product):
    response = client.get("/products")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "T-Shirt"
    assert response.json()[0]["price"] == 29.99
    assert "specifications" not in response.json()[0]

def test_get_product(add_product):
    response = client.get(f"/product/{add_product['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "T-Shirt"
    assert response.json()["price"] == 29.99
    assert response.json()["specifications"]["size"] == "M"
    assert response.json()["specifications"]["color"] == "Red"
    assert response.json()["specifications"]["material"] == "Cotton"

def test_get_product_not_found():
    response = client.get("/product/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"

def test_get_product_invalid_id():
    response = client.get("/product/abc")
    assert response.status_code == 422