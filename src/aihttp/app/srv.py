import jinja2
import logging
from aiohttp import web
from aiohttp_jinja2 import setup as jinja_setup
from src.log import initial_logging
from src.aihttp.conf import settings
from src.aihttp.web.home.views import HomeView

def create_app():
    initial_logging()
    logger = logging.getLogger(settings.LOGGER)
    app = web.Application(logger=logger)
    app.router.add_route("GET",
                         "/",
                         HomeView)
    jinja2_setup(
        app,
        loader=jinja2.FileSystemLoader(
            list(settings.BASE_DIR.glob("**/web/**/templates"))
        )
    )
    return app
