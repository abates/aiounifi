"""Test client configuration API.

pytest --cov-report term-missing --cov=aiounifi.clients tests/test_clients.py
"""

from typing import Any

import pytest

from aiounifi.interfaces.clients import Clients
from aiounifi.models.api import ApiEndpoint

from tests.conftest import assert_handler_request


@pytest.mark.parametrize(
    ("method_name", "request_args", "api_request", "expected_error"),
    [
        (
            "send_cmd",
            {"cmd": "test-cmd", "arg1": 1, "arg2": 2},
            {
                "method": "post",
                "endpoint": ApiEndpoint(path="/cmd/stamgr"),
                "data": {
                    "cmd": "test-cmd",
                    "arg1": 1,
                    "arg2": 2,
                },
            },
            None,
        ),
        (
            "block",
            {"mac": "00:01:02:03:04:05"},
            {
                "method": "post",
                "endpoint": ApiEndpoint(path="/cmd/stamgr"),
                "data": {
                    "cmd": "block-sta",
                    "mac": "00:01:02:03:04:05",
                },
            },
            None,
        ),
        (
            "reconnect",
            {"mac": "00:01:02:03:04:05"},
            {
                "method": "post",
                "endpoint": ApiEndpoint(path="/cmd/stamgr"),
                "data": {
                    "cmd": "kick-sta",
                    "mac": "00:01:02:03:04:05",
                },
            },
            None,
        ),
        (
            "remove",
            {"macs": ["00:01:02:03:04:05"]},
            {
                "method": "post",
                "endpoint": ApiEndpoint(path="/cmd/stamgr"),
                "data": {
                    "cmd": "forget-sta",
                    "macs": ["00:01:02:03:04:05"],
                },
            },
            None,
        ),
        (
            "unblock",
            {"mac": "00:01:02:03:04:05"},
            {
                "method": "post",
                "endpoint": ApiEndpoint(path="/cmd/stamgr"),
                "data": {
                    "cmd": "unblock-sta",
                    "mac": "00:01:02:03:04:05",
                },
            },
            None,
        ),
    ],
)
async def test_clients(
    method_name: str,
    request_args: dict[str, Any],
    api_request: dict[str, Any],
    expected_error: type[Exception] | None,
):
    """Test device interface methods."""
    await assert_handler_request(
        Clients, method_name, request_args, api_request, expected_error
    )
