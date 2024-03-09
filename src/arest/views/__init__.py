from ._base import (
    AbstractJsonView,
    AbstractAuthView,
    AuthenticationError,
    AuthorizationError,
    web,
)


class JsonView(AbstractJsonView):
    def __await__(self):
        return super()._iter().__await__()


class AuthView(AbstractAuthView):
    def __await__(self):
        return self._iter().__await__()

    async def _iter(self):
        try:
            method = await super()._iter()
        except AuthenticationError as error:
            raise web.HTTPUnauthorized(reason=str(error))
        except AuthorizationError as error:
            raise web.HTTPForbidden(reason=str(error))
        return await method()
