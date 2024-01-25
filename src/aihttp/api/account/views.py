from aiohttp import web
from src.aihttp.api.account.models import User


class Account(web.View):
    async def get(self):
        return web.json_response({"message": "ok"})

    async def post(self):
        data = await self.request.json()
        user = User(**data)
        user.set_passwd()
        await user.save()
        return web.json_response({"uuid": user.uuid})

