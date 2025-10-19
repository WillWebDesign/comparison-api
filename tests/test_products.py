import shutil
import pytest
import os
from fastapi.testclient import TestClient
from app.main import app
from app.services.products_service import DATA_PATH

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_test_data(tmp_path):
  test_data_path = tmp_path / "products.json"
  shutil.copy(DATA_PATH, test_data_path)

  from app.services import products_service
  products_service.DATA_PATH = test_data_path

  yield

  if test_data_path.exists():
      test_data_path.unlink()

@pytest.fixture
def example_product():
  return {
    "name": "Test product",
    "description": "Product for test",
    "image_url": "https://example.com/",
    "price": 4599.0,
    "rating": 3,
    "specs": {
      "screen": ""
    }
  }

@pytest.fixture
def setup_test_datafile_error(tmp_path):
  bad_json = tmp_path / "products.json"
  bad_json.write_text("{ invalid json }")

  from app.services import products_service
  products_service.DATA_PATH = bad_json

@pytest.fixture
def setup_test_datafile_not_found(tmp_path):
  bad_path = tmp_path / "product_path_error.json"

  from app.services import products_service
  products_service.DATA_PATH = bad_path

@pytest.fixture
def setup_test_datafile_unable_save_data(tmp_path):
  test_data_path = tmp_path / "products.json"
  test_data_path.write_text("[]")
  os.chmod(test_data_path, 0o444)

  from app.services import products_service
  products_service.DATA_PATH = test_data_path

  yield

  os.chmod(test_data_path, 0o666)

def test_start_api():
  response = client.get("/")
  assert response.status_code == 200
  assert "api start" in response.json()["message"].lower()

def test_create_product(example_product):
  response = client.post("/api/products/", json=example_product)
  assert response.status_code == 201
  data = response.json()
  assert data["name"] == example_product["name"]
  assert "id" in data

def test_create_invalid_product():
  invalid_product = {
      "description": "Missing name",
      "price": -10,
      "image_url": "not_a_url"
  }
  response = client.post("/api/products/", json=invalid_product)
  assert response.status_code == 422

def test_create_product_datafile_error(example_product, setup_test_datafile_error):
  response = client.post("/api/products/", json=example_product)
  assert response.status_code == 500
  assert "Invalid data file format" in response.json()["detail"]

def test_get_all_products():
  response = client.get("/api/products/")
  assert response.status_code == 200
  data = response.json()
  assert isinstance(response.json(), list)
  assert len(data) > 0
  assert "id" in data[0]

def test_get_all_datafile_error(setup_test_datafile_error):
  response = client.get("/api/products/")
  assert response.status_code == 500
  assert "Invalid data file format" in response.json()["detail"]

def test_get_product(example_product):
  created = client.post("/api/products/", json=example_product).json()
  product_id = created["id"]
  response = client.get(f"/api/products/{product_id}")
  assert response.status_code == 200
  data = response.json()
  assert data["name"] == example_product["name"]
  assert "id" in data

def test_get_product_not_found():
  response = client.get("/api/products/0")
  assert response.status_code == 404
  assert "detail" in response.json()

def test_update_product_put(example_product):
  created = client.post("/api/products/", json=example_product).json()
  product_id = created["id"]

  update_data = {**example_product, "price": 25.99}
  response = client.put(f"/api/products/{product_id}", json=update_data)
  assert response.status_code == 200
  assert response.json()["price"] == 25.99

def test_update_product_put_datafile_error(example_product, setup_test_datafile_error):
  update_data = {**example_product, "price": 25.99}
  response = client.put(f"/api/products/0", json=update_data)
  assert response.status_code == 500
  assert "Invalid data file format" in response.json()["detail"]

def test_update_non_existing_product_put(example_product):
  response = client.put("/api/products/0", json=example_product)
  assert response.status_code == 404
  assert "not found" in response.json()["detail"].lower()

def test_update_product_patch(example_product):
  created = client.post("/api/products/", json=example_product).json()
  product_id = created["id"]

  patch_data = {"description": "Updated description"}
  response = client.patch(f"/api/products/{product_id}", json=patch_data)
  assert response.status_code == 200
  assert response.json()["description"] == "Updated description"

def test_update_product_patch_datafile_error(setup_test_datafile_error):
  response = client.patch(f"/api/products/0", json={})
  assert response.status_code == 500
  assert "Invalid data file format" in response.json()["detail"]

def test_update_non_existing_product_patch(example_product):
  response = client.patch("/api/products/0", json=example_product)
  assert response.status_code == 404
  assert "not found" in response.json()["detail"].lower()

def test_delete_product(example_product):
  created = client.post("/api/products/", json=example_product).json()
  product_id = created["id"]

  response = client.delete(f"/api/products/{product_id}")
  assert response.status_code == 204

  # Verify it's goneC
  get_response = client.get(f"/api/products/{product_id}")
  assert get_response.status_code == 404

def test_delete_non_existing_product():
  response = client.delete("/api/products/0")
  assert response.status_code == 404
  assert "not found" in response.json()["detail"].lower()

def test_delete_product_datafile_error(setup_test_datafile_error):
  response = client.delete(f"/api/products/0")
  assert response.status_code == 500
  assert "Invalid data file format" in response.json()["detail"]

def test_datafile_not_found(setup_test_datafile_not_found):
  response = client.get("/api/products/")
  data = response.json()
  assert response.status_code == 200
  assert data == []

def test_unable_save_data(example_product, setup_test_datafile_unable_save_data):
  response = client.post("/api/products/", json=example_product)
  assert response.status_code == 500
  data = response.json()
  assert "detail" in data
  assert "unable to save data" in data["detail"].lower()
