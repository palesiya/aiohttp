from typing import TypeAlias
from tortoise import models, fields
from tortoise.queryset import QuerySet
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

TModel: TypeAlias = models.Model


class BaseModel(models.Model):
    uuid = fields.UUIDField(pk=True)
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True

    @classmethod
    async def serialize(cls, instance: TModel | QuerySet, **kwargs):
        if isinstance(instance, TModel):
            serializer = pydantic_model_creator(cls, **kwargs)
            data = await serializer.from_tortoise_orm(instance)
        elif isinstance(instance, QuerySet):
            serializer = pydantic_queryset_creator(cls, **kwargs)
            data = await serializer.from_queryset(instance)
        else:
            raise TypeError("Invalid type for instance")
        return data.model_dump()

    @property
    def is_saved(self):
        return self._saved_in_db
