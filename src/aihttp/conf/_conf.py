import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.absolute()

DEBUG = True
if DEBUG:
    LOGGER = "dev"
else:
    LOGGER = "prod"

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
        "account": {"models": ["src.aihttp.api.account.models", "aerich.models"],
                    "default_connection": "default"},
    },
    "use_tz": False,
    "timezone": "UTC",
}

HOST = ""
SECRET_KEY = ""
