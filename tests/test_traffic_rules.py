"""Test traffic routes API for disabling and enabling traffic routes.

pytest --cov-report term-missing --cov=aiounifi.traffic_route tests/test_traffic_routes.py
"""

from typing import Any

import pytest

from aiounifi.interfaces.traffic_rules import TrafficRules
from aiounifi.models.traffic_rule import TrafficRule

from tests.conftest import assert_handler_request


@pytest.mark.parametrize(
    ("method_name", "method_args", "expected_request", "expected_error"),
    [
        (
            "save",
            {
                "api_item": TrafficRule(id="traffic_rule_1"),
            },
            {
                "method": "put",
                "endpoint": TrafficRules.update_endpoint,
                "api_item": TrafficRule(id="traffic_rule_1"),
                "data": {"_id": "traffic_rule_1"},
            },
            None,
        ),
        (
            "enable",
            {
                "traffic_rule": TrafficRule(id="traffic_rule_1", enabled=False),
            },
            {
                "method": "put",
                "endpoint": TrafficRules.update_endpoint,
                "api_item": TrafficRule(id="traffic_rule_1", enabled=True),
                "data": {"_id": "traffic_rule_1", "enabled": True},
            },
            None,
        ),
        (
            "disable",
            {
                "traffic_rule": TrafficRule(id="traffic_rule_1", enabled=True),
            },
            {
                "method": "put",
                "endpoint": TrafficRules.update_endpoint,
                "api_item": TrafficRule(id="traffic_rule_1", enabled=False),
                "data": {"_id": "traffic_rule_1", "enabled": False},
            },
            None,
        ),
    ],
)
async def test_traffic_rules(
    method_name: str,
    method_args: dict[str, Any],
    expected_request: dict[str, Any],
    expected_error: type[Exception] | None,
):
    """Test device interface methods."""
    await assert_handler_request(
        TrafficRules,
        method_name,
        method_args,
        expected_request,
        expected_error,
    )
