from aiohttp import web
from src.aihttp.app.srv import create_app


web.run_app(create_app(), host="127.0.0.1", port=8000)
