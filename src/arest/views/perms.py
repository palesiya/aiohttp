from arest.views._base import AbstractPermission, Request, AnonymousUser
from arest.exceptions import AuthenticationError


class AnonymousPermission(AbstractPermission):
    @classmethod
    async def process_token(cls, request: Request):
        return AnonymousUser()


class SimplePermission(AbstractPermission):
    ...


class AdminPermission(AbstractPermission):
    @classmethod
    async def process_token(cls, request: Request):
        user = await super().process_token(request)
        if user.is_admin:
            return user
        raise AuthenticationError("Permission Denied")


def permission(permission_class):
    def _handler(cls_view):
        for meth_name in ("get", "post", "put", "delete"):
            meth = getattr(cls_view, meth_name, None)
            if meth is not None and not hasattr(meth, "__perm_cls__"):
                setattr(meth, "__perm_cls__", permission_class)
        return cls_view

    return _handler


def sub_permission(permission_class):
    def _handler(func):
        setattr(func, "__perm_cls__", permission_class)
        return func

    return _handler
