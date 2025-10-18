from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, Dict

class ProductBase(BaseModel):
  name: str = Field(..., description="Product name")
  description: str = Field(..., description="Short description of product")
  image_url: HttpUrl = Field(..., description="Image of product")
  price: float = Field(..., description="Price product in USD")
  rating: Optional[float] = Field(None, ge=0, le=5, description="Average rating (0-5)")
  specs: Optional[Dict[str, str]]= Field(
    default_factory=dict, description="Specifications of product"
  )

class Product(ProductBase):
  id: int = Field(..., description="Inique identifier of the product")

class ProductCreate(ProductBase):
  pass

class ProductPut(ProductBase):
  rating: Optional[float] = Field(..., ge=0, le=5, description="Average rating (0-5)")
  specs: Optional[Dict[str, str]]= Field(
    ..., description="Specifications of product"
  )

class ProductPatch(BaseModel):
  name: str = Field(None, description="Product name")
  description: str = Field(None, description="Short description of product")
  image_url: HttpUrl = Field(None, description="Image of product")
  price: float = Field(None, description="Price product in USD")
  rating: Optional[float] = Field(None, ge=0, le=5, description="Average rating (0-5)")
  specs: Optional[Dict[str, str]]= Field(
    default_factory=dict, description="Specifications of product"
  )
