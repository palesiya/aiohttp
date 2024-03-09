import os
import pathlib
from typing import Callable
from collections import namedtuple
from datetime import date

from tortoise import fields
from tortoise.signals import post_delete
from arest.db import BaseModel
from arest.conf import settings

# file_field = namedtuple("File", ("path", "url"))


class Follow(BaseModel):
    file = fields.ForeignKeyField("file.File", related_name="follow")
    user = fields.ForeignKeyField("account.User", related_name="follows")
    close = fields.DatetimeField(null=True)
    share = fields.BooleanField(default=True)

    class Meta:
        table = "follows"


class FileField(fields.TextField):
    def __init__(
        self, upload_to: Callable = lambda instance, filename: filename, **kwargs
    ):
        super().__init__(**kwargs)
        self._upload_to = upload_to

    def to_db_value(self, value: pathlib.Path, instance: BaseModel) -> str:
        value = value.relative_to(settings.STORAGE_DIR)
        value = super().to_db_value(value, instance)
        return value

    def to_python_value(self, value: str) -> pathlib.Path:
        check_path: pathlib.Path = settings.STORAGE_DIR / value
        if not check_path.exists():
            value = self._upload_to(value)
        value = super().to_python_value(value)
        res = settings.STORAGE_DIR / value
        res.parent.mkdir(parents=True, exist_ok=True)
        return res


class File(BaseModel):
    @staticmethod
    def make_filename(filename: str) -> pathlib.Path:
        path = pathlib.Path(date.today().strftime("%Y/%m/%d/"))
        return path / os.urandom(24).hex()

    filename = fields.CharField(max_length=256)
    path = FileField(upload_to=make_filename)
    size = fields.BigIntField()
    owner = fields.ForeignKeyField(
        "account.User", on_delete=fields.CASCADE, related_name="files"
    )

    def url(self) -> str:
        return f"/{self.uuid}/{self.filename}"

    class Meta:
        table = "files"

    class PydanticMeta:
        exclude = ("path",)
        computed = ("url",)


@post_delete(File)
async def file_clear(sender, instance, using_db):
    ...
