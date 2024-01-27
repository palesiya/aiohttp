import jinja2
import logging
from aiohttp import web
from aiohttp_jinja2 import setup as jinja_setup
from src.log import initial_logging
from src.aihttp.conf import settings
from controller import controller_setup
from tortoise.contrib.aiohttp import register_tortoise


def create_app():
    initial_logging()
    logger = logging.getLogger(settings.LOGGER)
    app = web.Application(logger=logger)
    controller_setup(app, "aihttp.web.urls")
    jinja_setup(
        app,
        loader=jinja2.FileSystemLoader(
            list(settings.BASE_DIR.glob("web/**/templates"))
        )
    )
    register_tortoise(app, config=settings.DATABASE, generate_schemas=True)

    return app
