"""Test DPI configuration API.

pytest --cov-report term-missing --cov=aiounifi.dpi tests/test_dpi.py
"""

from typing import Any

import pytest

from aiounifi.interfaces.dpi_restriction_apps import DPIRestrictionApps
from aiounifi.models.dpi_restriction_app import DPIRestrictionApp

from tests.conftest import assert_handler_request


@pytest.mark.parametrize(
    ("method_name", "request_args", "api_request", "expected_error"),
    [
        (
            "set_enabled",
            {
                "app": DPIRestrictionApp(id="TEST_APP_ID", enabled=False),
                "enabled": True,
            },
            {
                "method": "put",
                "endpoint": DPIRestrictionApps.update_endpoint,
                "data": {"enabled": True},
            },
            None,
        ),
        (
            "enable",
            {"app": DPIRestrictionApp(id="TEST_APP_ID", enabled=False)},
            {
                "method": "put",
                "endpoint": DPIRestrictionApps.update_endpoint,
                "data": {"enabled": True},
            },
            None,
        ),
        (
            "disable",
            {"app": DPIRestrictionApp(id="TEST_APP_ID", enabled=True)},
            {
                "method": "put",
                "endpoint": DPIRestrictionApps.update_endpoint,
                "data": {"enabled": False},
            },
            None,
        ),
    ],
)
async def test_dpi_apps(
    method_name: str,
    request_args: dict[str, Any],
    api_request: dict[str, Any],
    expected_error: type[Exception] | None,
):
    """Test device interface methods."""
    await assert_handler_request(
        DPIRestrictionApps, method_name, request_args, api_request, expected_error
    )
