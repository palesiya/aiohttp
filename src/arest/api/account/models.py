import base64
from tortoise import fields
from hashlib import sha3_256
import os

from arest.db import BaseModel
from arest.conf import settings


class User(BaseModel):
    @property
    def is_anonymous(self):
        return False

    username = fields.CharField(max_length=25, index=True, unique=True)
    email = fields.CharField(max_length=256)
    password = fields.TextField()
    is_active = fields.BooleanField(default=False)
    is_admin = fields.BooleanField(default=False)
    refresh = fields.TextField(null=True)

    def __str__(self):
        return self.username

    def set_password(self):
        salt = os.urandom(32)
        h_passwd = sha3_256(self.password.encode("utf-8")).digest()
        mix = bytes([p ^ s for p, s in zip(h_passwd, salt)])
        h_passwd = sha3_256(mix).digest()
        sk = sha3_256(settings.SECRET_KEY.encode("utf-8")).digest()
        mix = bytes([p ^ s for p, s in zip(h_passwd, sk)])
        h_passwd = sha3_256(mix).digest()
        self.password = f'{base64.b64encode(h_passwd).decode("utf-8")}.{base64.b64encode(salt).decode("utf-8")}'

    def check_passwd(self, row_passwd):
        hashed_pass, salt = self.password.split(".")
        salt = base64.b64decode(salt)
        h_passwd = sha3_256(row_passwd.encode("utf-8")).digest()
        mix = bytes([p ^ s for p, s in zip(h_passwd, salt)])
        h_passwd = sha3_256(mix).digest()
        sk = sha3_256(settings.SECRET_KEY.encode("utf-8")).digest()
        mix = bytes([p ^ s for p, s in zip(h_passwd, sk)])
        h_passwd = base64.b64encode(sha3_256(mix).digest()).decode("utf-8")

        if hashed_pass == h_passwd:
            return True
        return False

    class Meta:
        table = "users"

    class PydanticMeta:
        exclude = ("password", "is_active", "refresh")
