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
                "host": "@format {this.DB_HOST}",
                "port": "@format {this.DB_PORT}",
                "user": "@format {this.DB_USER}",
                "password": "@format {this.DB_PASS}",
                "database": "@format {this.DB_NAME}",
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
