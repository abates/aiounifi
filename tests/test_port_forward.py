"""Test port forwarding API."""

from typing import Any

import pytest

from aiounifi.interfaces.port_forwarding import PortForwarding
from aiounifi.models.port_forward import PortForward

from tests.conftest import assert_handler_request


@pytest.mark.parametrize(
    ("method_name", "request_args", "api_request", "expected_error"),
    [
        (
            "set_enabled",
            {
                "port_forward": PortForward(id="port-forward-1", enabled=False),
                "enabled": True,
            },
            {
                "method": "put",
                "endpoint": PortForwarding.update_endpoint,
                "data": {"enabled": True},
            },
            None,
        ),
        (
            "enable",
            {"port_forward": PortForward(id="port-forward-1", enabled=False)},
            {
                "method": "put",
                "endpoint": PortForwarding.update_endpoint,
                "data": {"enabled": True},
            },
            None,
        ),
        (
            "disable",
            {"port_forward": PortForward(id="port-forward-1", enabled=True)},
            {
                "method": "put",
                "endpoint": PortForwarding.update_endpoint,
                "data": {"enabled": False},
            },
            None,
        ),
    ],
)
async def test_port_fowarding(
    method_name: str,
    request_args: dict[str, Any],
    api_request: dict[str, Any],
    expected_error: type[Exception] | None,
):
    """Test device interface methods."""
    await assert_handler_request(
        PortForwarding, method_name, request_args, api_request, expected_error
    )
