from fastapi.encoders import jsonable_encoder
import json
import logging
from typing import List, Union
from app.models.product import (
  Product,
  ProductCreate,
  ProductPut,
  ProductPatch
)
from pathlib import Path

logger = logging.getLogger(__name__)

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "products.json"
# DATA_PATH = "app/data/products.json"

# Custom exceptions for a domain
class ProductNotFoundError(Exception):
  """Raised when product not exits or cannot be found"""
  pass

class DataFileError(Exception):
  """Raised when there is a problem with the data file"""
  pass

class ProductService:

  # Methods for read n' write data file

  @classmethod
  def _load_data(cls) -> List[dict]:
    try:
      with open(DATA_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)
        logger.debug(f"{len(data)} items load form data file")
        return data
    except FileNotFoundError:
      logger.warning("Data file not found | Return a empty list")
      return []
    except json.JSONDecodeError as err:
      logger.error(f"Error in data file: {err}")
      raise DataFileError("Invalid data file format")

  @classmethod
  def _save_data(cls, data: List[dict]):
    try:
      serializable_date = jsonable_encoder(data)
      with open(DATA_PATH, "w", encoding="utf-8") as file:
        json.dump(serializable_date, file, indent=2, ensure_ascii=False)
      logger.info(f"Saved {len(data)} items in data file")
    except Exception as err:
      logger.exception(f"Failed to save data: {err}")
      raise DataFileError("Unable to save data")

  # CRUD

  @classmethod
  def get_all(cls) -> List[Product]:
    logger.info("Fetching all products...")
    return [Product(**item) for item in cls._load_data()]

  @classmethod
  def get_by_id(cls, product_id: int) -> Product:
    logger.info(f"Fetching produc by id={product_id}")
    products = cls._load_data()
    product = next((product for product in products if product["id"] == product_id), None)
    if not product:
      logger.warning(f"Product not found. Product id = {product_id}")
      raise ProductNotFoundError(f"Product with id={product_id} not found")
    return Product(**product)

  @classmethod
  def create(cls, product: ProductCreate) -> Product:
    logger.info(f"Creating product: {product.name}")
    products = cls._load_data()
    new_id = max((p["id"] for p in products), default=0) + 1
    new_product = product.model_dump()
    new_product["id"] = new_id
    products.append(new_product)
    cls._save_data(products)
    logger.debug(f"Product created with id={new_id}")
    return Product(**new_product)

  @classmethod
  def update(cls, product_id: int, updated_product: Union[ProductPut, ProductPatch]) -> Product:
    logger.info(f"Updatign product: {product_id}")
    products = cls._load_data()
    product = next((product for product in products if product["id"] == product_id), None)
    if not product:
      logger.warning(f"Attempted to update non-existing product id={product_id}")
      raise ProductNotFoundError(f"Product with id {product_id} not found")

    if isinstance(updated_product, ProductPut):
      product_copy = {"id": product_id}
    else:
      product_copy = product.copy()

    updated_data = updated_product.model_dump(exclude_unset=True)
    updated_data.pop("id", None)
    product_copy.update(updated_data)

    products[products.index(product)] = product_copy
    cls._save_data(products)

    logger.info(
      f"Product updated successfully -> id={product_id} with fields={list(updated_data.keys())}"
    )
    return Product(**product_copy)

  @classmethod
  def delete(cls, product_id: int) -> None:
    logger.info(f"Deleting product: {product_id}")
    products = cls._load_data()
    filtered_products = [product for product in products if product["id"] != product_id]
    if len(filtered_products) == len(products):
      logger.warning(f"Attemped to delete non-existing poduct id={product_id}")
      raise ProductNotFoundError(f"Product with id {product_id} not found")
    cls._save_data(filtered_products)
    logger.info(f"Product deleted successfully -> id={product_id}")
