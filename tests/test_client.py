from http import HTTPStatus
import json
from typing import Any
from unittest.mock import AsyncMock, Mock, PropertyMock, call, patch

import pytest

from aiounifi import errors
from aiounifi.client import UnifiClient
from aiounifi.models.api import ApiEndpoint
from aiounifi.models.configuration import Configuration


@pytest.mark.parametrize(
    ("method_name", "method_args"),
    [
        ("login", []),
        ("endpoint_request", ["GET", None]),
        ("start_websocket", []),
        ("is_unifi_os", []),
    ],
)
def test_session_initialized(method_name, method_args):
    """Confirm methods raise NotConnectedError if the session has not been initialized."""
    client = UnifiClient(Configuration("host", username="user", password="pass"))
    with pytest.raises(errors.NotConnectedError):
        getattr(client, method_name)(*method_args)


@pytest.mark.parametrize(
    ("status_code", "expected_value", "expected_error"),
    [
        (HTTPStatus.OK, True, None),
        (HTTPStatus.FOUND, False, None),
        (HTTPStatus.NOT_FOUND, False, errors.AiounifiException),
    ],
)
async def test_connect(
    status_code: int, expected_value: bool, expected_error: type | None
):
    """Confirm the connect method correctly detects unifi os."""
    with patch(
        "aiounifi.client.aiohttp.ClientSession.get", new_callable=AsyncMock
    ) as get_method:
        response = Mock()
        type(response).status = PropertyMock(return_value=status_code)
        get_method.return_value = response
        client = UnifiClient(Configuration("host", username="user", password="pass"))
        if expected_error:
            with pytest.raises(expected_error):
                await client.connect()
            assert hasattr(client, "session") is False
        else:
            await client.connect()
            assert client.is_unifi_os == expected_value
            assert client.session is not None


@pytest.mark.parametrize(
    ("is_unifi_os", "response", "response_data", "expected_headers", "expected_error"),
    [
        (
            False,
            {"content_type": "text/html", "headers": {}},
            {},
            {},
            errors.RequestError,
        ),
        (False, {"content_type": "application/json", "headers": {}}, {}, {}, None),
        (
            True,
            {
                "content_type": "application/json",
                "headers": {"x-csrf-token": "token123"},
            },
            {},
            {"x-csrf-token": "token123"},
            None,
        ),
        (
            True,
            {
                "content_type": "application/json",
                "headers": {"x-csrf-token": "token123"},
            },
            {"meta": {"rc": "error", "msg": "api.err.Invalid"}},
            {},
            errors.Unauthorized,
        ),
    ],
)
async def test_login(
    is_unifi_os,
    response,
    response_data,
    expected_headers: dict[str, Any],
    expected_error: type | None,
):
    """Verify login works as expected."""
    post_response = Mock()
    for key, value in response.items():
        setattr(type(post_response), key, PropertyMock(return_value=value))
    post_response.json = AsyncMock(return_value=response_data)
    post_response.read = AsyncMock(return_value=json.dumps(response_data))
    session = AsyncMock()
    type(session).headers = PropertyMock(return_value={})
    session.post.return_value = post_response
    client = UnifiClient(Configuration("host", username="user", password="pass"))
    client.session = session
    client._is_unifi_os = is_unifi_os
    if expected_error:
        with pytest.raises(expected_error):
            await client.login()
    else:
        await client.login()
        expected_json = {
            "username": "user",
            "password": "pass",
            "rememberMe": True,
        }
        if is_unifi_os:
            session.post.assert_called_with(
                "https://host:8443/api/auth/login", json=expected_json
            )
        else:
            session.post.assert_called_with(
                "https://host:8443/api/login", json=expected_json
            )

        assert expected_headers == session.headers


@pytest.mark.parametrize(
    ("method_name", "call_args"),
    [
        ("get", {"endpoint": "endpoint", "api_item": "api_item"}),
        (
            "post",
            {
                "endpoint": "endpoint",
                "api_item": "api_item",
                "data": {"post": "some data"},
            },
        ),
        (
            "put",
            {
                "endpoint": "endpoint",
                "api_item": "api_item",
                "data": {"put": "some other data"},
            },
        ),
    ],
)
async def test_client_methods(method_name, call_args):
    """Confirm helper methods pass-through arguments."""
    client = UnifiClient(Configuration("host", username="user", password="pass"))
    client.session = Mock()
    client.endpoint_request = AsyncMock(return_value="test value")
    return_value = await getattr(client, method_name)(**call_args)
    assert return_value == "test value"
    client.endpoint_request.assert_called_with(method=method_name, **call_args)


async def test_endpoint_request():
    client = UnifiClient(Configuration("host", username="user", password="pass"))
    response = AsyncMock()
    response.__aenter__.return_value = response
    response.__aexit__.return_value = None
    response.json.return_value = {}
    client.session = Mock(request=Mock(return_value=response))

    # normal request, already authenticated
    await client.endpoint_request("get", ApiEndpoint(path="/endpoint"))
    client.session.request.assert_called_with(
        method="get", url="/api/s/default/endpoint", json=None, ssl=False
    )

    # auth session expired, need to relogin
    def _response(*args, **kwargs):
        yield errors.LoginRequired
        yield response

    response.reset_mock()
    response.__aenter__.side_effect = _response()
    response.__aexit__.return_value = None
    client.session = Mock(request=Mock(return_value=response))
    client.login = AsyncMock()

    await client.endpoint_request("get", ApiEndpoint(path="/endpoint"))
    client.login.assert_called_once()
    client.session.request.assert_has_calls(
        [
            call(method="get", url="/api/s/default/endpoint", json=None, ssl=False),
            call(method="get", url="/api/s/default/endpoint", json=None, ssl=False),
        ]
    )
