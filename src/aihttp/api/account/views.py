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


class Auth(web.View):
    async def post(self):
        data = await self.request.json()
        user = await User.get(username=data["username"])
        if user.check_passwd(data["password"]):
            return web.json_response({"msg": "ok"})
        return web.json_response({"msg": "not found"}, status=401)


