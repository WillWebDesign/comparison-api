from fastapi import FastAPI
from app.api.routes import products
from app.utils.config import settings
from app.core import logger

app = FastAPI(
  title=settings.app_name,
  version=settings.app_version,
  description=settings.app_description
)

app.include_router(products.router, prefix="/api")

@app.get("/", summary="Health check", tags=["System"])
def root():
  return {"message": f"Api start {settings.app_name}"}
