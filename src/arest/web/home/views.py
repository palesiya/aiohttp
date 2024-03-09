from aiohttp import web
from aiohttp_jinja2 import template
from arest.api.account.models import User


class HomeView(web.View):
    @template("home.html")
    async def get(self):
        return {"msg": "Hello Python!"}


class AboutView(web.View):
    @template("about.html")
    async def get(self):
        return {"data": "We are very good company!"}


class ContactView(web.View):
    @template("contact.html")
    async def get(self):
        return {"number": "5544332211", "city": "New-York"}


class ActivateView(web.View):
    @template("activate.html")
    async def get(self):
        activate_token = self.request.match_info["activate_token"]
        user = await User.get_or_none(is_active=False, refresh=activate_token)
        if user is not None:
            user.refresh = None
            user.is_active = True
            await user.save(update_fields=("refresh", "is_active"))
            return {}
        raise web.HTTPNotFound(reason="User Not Found")
