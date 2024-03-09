class BaseArestException(RuntimeError):
    ...


class AuthorizationError(BaseArestException):
    """Comment"""


class AuthenticationError(BaseArestException):
    ...
