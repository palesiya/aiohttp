import json
from datetime import datetime, date
from enum import Enum
from abc import abstractmethod

import jwt
from typing import TypeAlias, Optional, Callable, Awaitable
from aiohttp import web, web_response, hdrs

from tortoise import exceptions as exc
from arest.conf import settings
from arest.api.account.models import User
from arest.exceptions import AuthenticationError, AuthorizationError

Request: TypeAlias = web.Request
StreamResponse: TypeAlias = web_response.StreamResponse


class DataEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (datetime, date)):
            return o.isoformat()
        if isinstance(o, Enum):
            return o.name
        return str(o)


def serrialize(data):
    return json.dumps(data, cls=DataEncoder)


class AnonymousUser:
    __slots__ = ()
    username = None
    is_anonymous = True
    is_admin = False
    uuid = None


ERROR_MAP = {
    exc.DoesNotExist: web.HTTPNotFound.status_code,
    exc.IntegrityError: web.HTTPBadRequest.status_code,
    ValueError: web.HTTPServerError.status_code,
    TypeError: web.HTTPBadRequest.status_code,
    Exception: web.HTTPServerError.status_code,
    AuthenticationError: web.HTTPUnauthorized.status_code,
    AuthorizationError: web.HTTPForbidden.status_code,
    json.JSONDecodeError: web.HTTPBadRequest.status_code,
    jwt.PyJWTError: web.HTTPUnauthorized.status_code,
}


class _AbstractView(web.View):
    @abstractmethod
    def __await__(self):
        ...

    async def _iter(self):
        if self.request.method not in hdrs.METH_ALL:
            self._raise_allowed_methods()
        method: Optional[Callable[[], Awaitable[StreamResponse]]]
        method = getattr(self, self.request.method.lower(), None)
        if method is None:
            self._raise_allowed_methods()
        return method


class AbstractAuthView(_AbstractView):
    @abstractmethod
    def __await__(self):
        ...

    async def _iter(self):
        method = await super()._iter()
        if hasattr(method, "__perm_cls__"):
            self.user = await method.__perm_cls__.process_token(self.request)
        return method


class AbstractJsonView(AbstractAuthView):
    @abstractmethod
    def __await__(self):
        ...

    def __init__(self, request: web.Request):
        super().__init__(request)
        self._user = AnonymousUser()

    @property
    def user(self) -> User | AnonymousUser:
        return self._user

    @user.setter
    def user(self, val):
        self._user = val

    @user.deleter
    def user(self):
        self._user = AnonymousUser()

    @staticmethod
    def _handle_exception(error: Exception):
        return ERROR_MAP[type(error)]

    async def _iter(self) -> StreamResponse:
        try:
            method = await super()._iter()
            result = await method()
        except Exception as error:
            status = self._handle_exception(error)
            msg = str(error)
            result = {"message": msg}
        else:
            status = (
                web.HTTPCreated.status_code
                if self.request.method == hdrs.METH_POST
                else web.HTTPOk.status_code
            )
        return web.json_response(result, status=status, dumps=serrialize)


class AbstractPermission:
    @staticmethod
    def get_token(request: Request):
        try:
            schema, token = request.headers["Authorization"].split(" ")
        except KeyError:
            raise AuthorizationError("Required 'Authorization' header")
        except ValueError:
            raise AuthorizationError("Required token schema")
        if schema != "Bearer":
            raise AuthorizationError("Unsupported token schema")
        return token

    @classmethod
    async def process_token(cls, request: Request):
        token = cls.get_token(request)
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, issuer="access", algorithms=["HS256"]
            )
        except (jwt.ExpiredSignatureError, jwt.DecodeError) as error:
            raise AuthorizationError(*error.args)
        except (jwt.InvalidIssuerError, jwt.InvalidSignatureError) as error:
            raise AuthenticationError(*error.args)
        user = await User.get(uuid=payload["uuid"], is_active=True)
        if user.refresh is not None and user.refresh == payload["tid"]:
            return user
        raise AuthenticationError("Permission Denied")
