from fastapi import APIRouter, status, HTTPException
from typing import List
from app.models.product import (
  Product,
  ProductCreate,
  ProductPut,
  ProductPatch
)
from app.models.error_response import ErrorResponse
from app.services.products_service import (
  ProductService,
  DataFileError,
  ProductNotFoundError
)

responses_common = {
    404: {
        "model": ErrorResponse,
        "description": "Product not found",
        "content": {
            "application/json": {
                "example": {"detail": "Product with id=123 not found"}
            }
        },
    },
    500: {
        "model": ErrorResponse,
        "description": "Internal server error",
        "content": {
            "application/json": {
                "example": {"detail": "Invalid data file format"}
            }
        },
    },
}

router = APIRouter(prefix="/products", tags=["Products"])

@router.get(
  "/",
  summary="Get all products",
  response_model=List[Product],
  responses=responses_common
)
def get_products():
  try:
    return ProductService.get_all()
  except DataFileError as err:
    raise HTTPException(status_code=500, detail=str(err))

@router.get(
  "/{product_id}",
  summary="Get product by id",
  response_model=Product,
  responses=responses_common
)
def get_product(product_id: int):
  try:
    return ProductService.get_by_id(product_id)
  except ProductNotFoundError as err:
    raise HTTPException(status_code=404, detail=str(err))

@router.post(
  "/",
  summary="Create a product",
  response_model=Product,
  status_code=status.HTTP_201_CREATED,
  responses=responses_common
)
def create_product(product: ProductCreate):
  try:
    return ProductService.create(product)
  except DataFileError as err:
    raise HTTPException(status_code=500, detail=str(err))

@router.put(
  "/{product_id}",
  summary="Update a product (Full)",
  response_model=Product,
  responses=responses_common
)
def update_product_put(product_id: int, product: ProductPut):
  try:
    return ProductService.update(product_id, product)
  except ProductNotFoundError as err:
    raise HTTPException(status_code=404, detail=str(err))
  except DataFileError as err:
    raise HTTPException(status_code=500, detail=str(err))

@router.patch(
  "/{product_id}",
  summary="Update a product (Partial)",
  response_model=Product,
  responses=responses_common
)
def update_product_patch(product_id: int, product: ProductPatch):
  try:
    return ProductService.update(product_id, product)
  except ProductNotFoundError as err:
    raise HTTPException(status_code=404, detail=str(err))
  except DataFileError as err:
    raise HTTPException(status_code=500, detail=str(err))

@router.delete(
  "/{product_id}",
  summary="Delete a product",
  status_code=status.HTTP_204_NO_CONTENT,
  responses=responses_common
)
def delete_product(product_id: int):
  try:
    return ProductService.delete(product_id)
  except ProductNotFoundError as err:
    raise HTTPException(status_code=404, detail=str(err))
  except DataFileError as err:
    raise HTTPException(status_code=500, detail=str(err))
