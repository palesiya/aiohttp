from pathlib import Path
from src.aihttp.conf import settings


settings.BASE_DIR = Path(__file__).parent.parent.absolute()

DEBUG = True
if DEBUG:
    LOGGER = "dev"
else:
    LOGGER = "prod"

DATABASE = {}
HOST = ""
SECRET_KEY = ""
