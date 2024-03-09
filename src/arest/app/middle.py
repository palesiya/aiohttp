from aiohttp import web, hdrs


class MiddleAuth:
    def __init__(self, api_path: str = "/api/"):
        self._api_path = api_path

    def get_middle(self):
        @web.middleware
        async def check(request, handler):
            if request.method in [
                hdrs.METH_GET,
                hdrs.METH_POST,
                hdrs.METH_PUT,
                hdrs.METH_DELETE,
            ]:
                print(self._api_path)
                token = request.headers.get("Authorization", "Not found token")
                print(token)
            return await handler(request)

        return check
