"""Library to communicate with a UniFi controller."""

from .controller import Controller
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
    "Controller",
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
