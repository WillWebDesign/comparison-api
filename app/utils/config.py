from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseModel):
  app_name: str = os.getenv("APP_NAME", "Comparison API")
  app_version: str = os.getenv("APP_VERSION", "1.0.0")
  app_description: str = os.getenv(
    "APP_DESCRIPTION", "Simplified backend API for comparing products(Items)items."
  )
  host: str = os.getenv("HOST", "127.0.0.1")
  port: int = os.getenv("PORT", 8000)
  reload: bool = os.getenv("RELOAD", True).lower() == "true"

settings = Settings()
