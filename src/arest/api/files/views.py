import aiofiles as af
from aiohttp import web
from arest.views import JsonView, AuthView
from arest.api.files.models import File, Follow
from arest.views import perms
from tortoise.expressions import Q


@perms.permission(perms.SimplePermission)
class FileView(JsonView):
    async def get(self):
        files = File.filter(
            Q(owner=self.user.uuid) | Q(follow__user=self.user, follow__share=True)
        )

        return await File.serialize(
            files,
            exclude=(
                "owner.email",
                "owner.is_admin",
                "owner.created",
                "owner.updated",
                "owner.follows",
                "follow",
            ),
        )

    async def post(self):
        data = await self.request.post()
        file_data = data.get("file_name")
        size = file_data.file.seek(0, 2)
        file_data.file.seek(0)
        new_file = File(
            filename=file_data.filename,
            path=file_data.filename,
            owner=self.user,
            size=size,
        )
        await new_file.save()
        async with af.open(new_file.path, mode="wb") as file:
            await file.write(file_data.file.read())
        return {"msg": "ok"}


@perms.permission(perms.SimplePermission)
class FollowView(JsonView):
    async def post(self):
        file_uuid = self.request.match_info["file_uuid"]
        data = await self.request.json()
        follows = [
            Follow(file_id=file_uuid, user_id=user_uuid) for user_uuid in data["users"]
        ]
        await Follow.bulk_create(follows)
        return {"msg": "Ok"}


@perms.permission(perms.SimplePermission)
class DownloadView(AuthView):
    async def get(self):
        file_uuid = self.request.match_info["file_uuid"]
        file = await File.get(
            Q(owner=self.user.uuid) | Q(follow__user=self.user, follow__share=True),
            uuid=file_uuid,
        )
        print(file.filename)
        return web.Response(text="Response")
