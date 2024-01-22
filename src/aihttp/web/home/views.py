from aiohttp import web
from aiohttp_jinja2 import template


class HomeView(web.View):

    @template("home.html")
    async def get(self):
        return {"msg": "hi"}
