import uuid
import jwt
import asyncio
import aiosmtplib
from datetime import datetime, timedelta
from email.message import EmailMessage

from arest.api.account.models import User
from arest.conf import settings
from arest.views import JsonView
from arest.views import perms
from arest.exceptions import AuthenticationError


async def send_email(data: dict):
    message = EmailMessage()
    message["From"] = "d.a.xolloo@gmail.com"
    message["To"] = data["email"]
    message["Subject"] = data["subject"]
    message.set_content(data["msg"])
    await aiosmtplib.send(
        message,
        hostname="smtp.gmail.com",
        port=587,
        username="d.a.xolloo@gmail.com",
        password=settings.GMAIL,
    )


@perms.permission(perms.SimplePermission)
class Account(JsonView):
    async def get(self):
        return await User.serialize(self.user)

    @perms.sub_permission(perms.AnonymousPermission)
    async def post(self):
        data = await self.request.json()
        new_usr = User(**data)
        new_usr.set_password()
        activate_id = str(uuid.uuid4())
        new_usr.refresh = activate_id
        await new_usr.save()
        # (settings.STORAGE_DIR / str(new_usr.uuid)).mkdir(exist_ok=True)
        # activate_link = f"http://127.0.0.1:8000/activate/{activate_id}"
        # email_data = {
        #     "email": new_usr.email,
        #     "subject": "Activate",
        #     "msg": activate_link,
        # }
        # asyncio.create_task(send_email(email_data)).add_done_callback(lambda x: x)
        return {"id": new_usr.uuid}

    async def put(self):
        ...

    async def delete(self):
        ...


class Token(JsonView):
    @staticmethod
    def on_update_user(task: asyncio.Task):
        try:
            _ = task.result()
        except asyncio.CancelledError as err:
            print(task.get_name())
        except Exception:
            print(task.get_name())

    def _gen_tokens(self, user) -> dict[str, str]:
        tid = str(uuid.uuid4())
        refresh = jwt.encode(
            {
                "uuid": str(user.uuid),
                "tid": tid,
                "exp": datetime.utcnow() + timedelta(days=7),
                "iss": "refresh",
            },
            settings.SECRET_KEY,
            algorithm="HS256",
        )
        access = jwt.encode(
            {
                "uuid": str(user.uuid),
                "tid": tid,
                "exp": datetime.utcnow() + timedelta(seconds=settings.EXP_TIME),
                "iss": "access",
            },
            settings.SECRET_KEY,
            algorithm="HS256",
        )
        user.refresh = tid
        asyncio.create_task(
            user.save(update_fields=("refresh",)), name=tid
        ).add_done_callback(self.on_update_user)
        return {"refresh": refresh, "access": access}

    async def post(self):
        data = await self.request.json()
        user = await User.get(username=data["username"], is_active=True)
        if user.check_passwd(data["password"]):
            return self._gen_tokens(user)
        await asyncio.sleep(3)
        raise AuthenticationError("Invalid password of username")

    async def put(self):
        data = await self.request.json()
        refresh = jwt.decode(
            data["refresh"],
            settings.SECRET_KEY,
            issuer="refresh",
            algorithms=["HS256"],
        )
        access = jwt.decode(
            data["refresh"],
            settings.SECRET_KEY,
            issuer="refresh",
            algorithms=["HS256"],
            options={"verify_signature": False},
        )
        user = await User.get(uuid=refresh["uuid"], is_active=True)
        if user.refresh is not None and (
            user.refresh == refresh["tid"] == access["tid"]
        ):
            return self._gen_tokens(user)
        raise AuthenticationError("Invalid tokens")

    @perms.sub_permission(perms.SimplePermission)
    async def delete(self):
        self.user.refresh = None
        await self.user.save(update_fields=("refresh",))
        return {"msg": "Ok"}
