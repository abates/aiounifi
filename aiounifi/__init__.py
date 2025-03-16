"""Library to communicate with a UniFi controller."""

from .client import UnifiClient
from .errors import (
    AiounifiException,
    BadGateway,
    Forbidden,
    LoginRequired,
    NoPermission,
    RequestError,
    ResponseError,
    ServiceUnavailable,
    TwoFaTokenRequired,
    Unauthorized,
    WebsocketError,
)

__all__ = [
    "UnifiClient",
    "AiounifiException",
    "BadGateway",
    "Forbidden",
    "LoginRequired",
    "NoPermission",
    "RequestError",
    "ResponseError",
    "ServiceUnavailable",
    "TwoFaTokenRequired",
    "Unauthorized",
    "WebsocketError",
]
