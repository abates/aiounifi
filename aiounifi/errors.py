"""Aiounifi errors."""

from http import HTTPStatus
from typing import Any

from aiohttp import ClientResponse


class AiounifiException(Exception):
    """Base error for aiounifi."""


class NotConnectedError(AiounifiException):
    """Raised when the client is not yet connected to the controller."""


class RequestError(AiounifiException):
    """Unable to fulfill request.

    Raised when host or API cannot be reached.
    """


class ResponseError(AiounifiException):
    """Invalid response."""


class NotFoundError(AiounifiException):
    """HTTP 404."""


class Unauthorized(AiounifiException):
    """Username is not authorized."""


class LoginRequired(AiounifiException):
    """User is logged out."""


class Forbidden(AiounifiException):
    """Forbidden request."""


class NoPermission(AiounifiException):
    """Users permissions are read only."""


class ServiceUnavailable(RequestError):
    """Service is unavailable.

    Common error if controller is restarting and behind a proxy.
    """


class BadGateway(RequestError):
    """Invalid response from the upstream server."""


class TwoFaTokenRequired(AiounifiException):
    """2 factor authentication token required."""


class WebsocketError(AiounifiException):
    """Websocket error."""


HTTP_ERRORS: dict[int, type] = {
    HTTPStatus.UNAUTHORIZED: LoginRequired,
    HTTPStatus.FORBIDDEN: Forbidden,
    HTTPStatus.NOT_FOUND: NotFoundError,
    HTTPStatus.BAD_GATEWAY: BadGateway,
    HTTPStatus.SERVICE_UNAVAILABLE: ServiceUnavailable,
    HTTPStatus.TOO_MANY_REQUESTS: ResponseError,
}

UNIFI_ERRORS = {
    "api.err.Invalid": Unauthorized,
    "api.err.LoginRequired": LoginRequired,
    "api.err.NoPermission": NoPermission,
    "api.err.Ubic2faTokenRequired": TwoFaTokenRequired,
}


def raise_for_unifi_error(version: int, response_data: dict[str, Any] | None):
    """Evaluate the response data and raise an error if one is present in the response."""
    if response_data:
        if version == 1 and response_data.get("meta", {}).get("rc") == "error":
            raise UNIFI_ERRORS.get(response_data["meta"]["msg"], AiounifiException)(
                response_data
            )
        elif version == 2 and "errorCode" in response_data:
            raise UNIFI_ERRORS.get(response_data["message"], AiounifiException)(
                response_data
            )


async def raise_for_status(response: ClientResponse) -> None:
    """Raise an error if the response status indicates an HTTP error."""
    error_cls = HTTP_ERRORS.get(response.status)

    if error_cls:
        raise error_cls(
            f"Received HTTP {response.status} for {response.request_info.url}"
        )

    response.raise_for_status()
