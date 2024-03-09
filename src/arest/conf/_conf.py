import os
import pathlib
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent.absolute()

DEBUG = True
if DEBUG:
    LOGGER = "dev"
    EXP_TIME = 60 * 60 * 24
    # EXP_TIME = 15
else:
    LOGGER = "prod"
    EXP_TIME = 120
DATABASE = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": os.getenv("DB_HOST"),
                "port": int(os.getenv("DB_PORT")),
                "user": os.getenv("DB_USER"),
                "password": os.getenv("DB_PASS"),
                "database": os.getenv("DB_NAME"),
            },
        }
    },
    "apps": {
        "account": {
            "models": ["arest.api.account.models", "aerich.models"],
            "default_connection": "default",
        },
        "file": {
            "models": ["arest.api.files.models"],
            "default_connection": "default",
        },
    },
    "use_tz": False,
    "timezone": "UTC",
}

HOST = ""
SECRET_KEY = ""

STORAGE_DIR = BASE_DIR / "storage"
STORAGE_URL = "/store"

# "/store/path/to/file.doc"
# BASE_DIR / "storage" / "path" / "to" / "file.doc"
#
# "path/to/file.doc"
