import base64
import os
from src.aihttp.conf import settings
from tortoise import models, fields
from hashlib import sha3_256
import asyncio


class BaseModel(models.Model):
    created = fields.DatetimeField(auto_now_add=True)
    uuid = fields.UUIDField(unique=True)
    update = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True

    @property
    def is_saved(self):
        return self._saved_in_db


class User(BaseModel):
    username = fields.CharField(max_length=25, index=True)
    email = fields.CharField(max_length=50)
    password = fields.BinaryField()
    is_active = fields.BooleanField(default=False)
    is_admin = fields.BooleanField(default=False)

    def __str__(self):
        return self.username

    def set_passwd(self):
        salt = os.urandom(32)
        h_passwd = sha3_256(self.password.encode("utf-8")).digest()
        mix = bytes([s ^ p for s, p in zip(salt, h_passwd)])
        h_passwd = sha3_256(mix).digest()
        sk = sha3_256(settings.SECRET_KEY.encode("utf-8")).digest()
        mix = bytes([s ^ p for s, p in zip(sk, h_passwd)])
        h_passwd = sha3_256(mix).digest()
        self.password = f'{base64.b64encode(h_passwd).decode("utf-8")}.{base64.b64encode(salt).decode("utf-8")}'

    async def check_passwd(self, row_passwd):
        hashed_pass, salt = self.password.split(".")
        h_passwd = sha3_256(row_passwd.encode("utf-8")).digest()
        mix = bytes([s ^ p for s, p in zip(salt, h_passwd)])
        h_passwd = sha3_256(mix).digest()
        sk = sha3_256(settings.SECRET_KEY.encode("utf-8")).digest()
        mix = bytes([s ^ p for s, p in zip(sk, h_passwd)])
        h_passwd = base64.b64encode(sha3_256(mix).digest()).decode("utf-8")
        if hashed_pass == h_passwd:
            return True
        return False

    class Meta:
        table = "users"
