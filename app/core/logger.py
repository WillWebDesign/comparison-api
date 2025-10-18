import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "app.log")

formatter = logging.Formatter(
  "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

#File
file_handler = RotatingFileHandler(
  LOG_FILE, maxBytes=1_000_000, backupCount=3, encoding="utf-8"
)
file_handler.setFormatter(formatter)

#Console
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

#Gloabal logger
logging.basicConfig(
  level=logging.INFO,
  handlers=[file_handler, console_handler]
)
