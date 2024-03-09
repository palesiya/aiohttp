import pathlib

import jinja2
from aiohttp_jinja2 import setup as jinja_setup
from aiohttp import web
import logging
from controller import controller_setup
from tortoise.contrib.aiohttp import register_tortoise
from log import initial_logging
from arest.conf import settings
from arest.app.middle import MiddleAuth


def create_app():
    initial_logging()
    logger = logging.getLogger(settings.LOGGER)
    logger.debug("TEST")
    app = web.Application(middlewares=[MiddleAuth(api_path="/api/").get_middle()])
    controller_setup(app, "arest.web.urls", True)
    jinja_setup(
        app,
        loader=jinja2.FileSystemLoader(
            list(settings.BASE_DIR.glob("web/**/templates"))
        ),
    )
    register_tortoise(app, config=settings.DATABASE, generate_schemas=True)
    storage_dir: pathlib.Path = settings.STORAGE_DIR
    storage_dir.mkdir(exist_ok=True)

    return app
