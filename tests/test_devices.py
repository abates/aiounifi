"""Test client configuration API.

pytest --cov-report term-missing --cov=aiounifi.devices tests/test_devices.py
"""

from typing import Any

import pytest

from aiounifi.interfaces.devices import Devices, _merge_overrides
from aiounifi.models.api import ApiEndpoint
from aiounifi.models.device import (
    Device,
    DeviceOutletOverrides,
    DevicePortOverrides,
    DeviceState,
    Outlet,
    Port,
)

from .fixtures import TEST_DEVICE_1

from tests.conftest import assert_handler_request


@pytest.mark.parametrize(
    ("obj", "expected"),
    [
        (
            Outlet(name="Outlet 1", relay_state=True),
            "<Outlet 1: relay state True>",
        ),
        (
            Outlet(name="Outlet 2", relay_state=False),
            "<Outlet 2: relay state False>",
        ),
        (Port(port_idx=1, poe_enable=True), "<Port 1: Poe True>"),
        (Port(port_idx=2, poe_enable=False), "<Port 2: Poe False>"),
        (
            Device(name="Device 1", mac="00:01:02:03:04:05"),
            "<Device Device 1: 00:01:02:03:04:05>",
        ),
    ],
)
def test_repr(obj, expected):
    """Test all of the __repr__ methods."""
    assert repr(obj) == expected


@pytest.mark.parametrize(
    ("existing_overrides", "new_overrides", "index_attr", "expected"),
    [
        (
            [],
            [DeviceOutletOverrides(cycle_enabled=True)],
            "index",
            [DeviceOutletOverrides(cycle_enabled=True)],
        ),
        (
            [
                DeviceOutletOverrides(index=1, cycle_enabled=False),
            ],
            [
                DeviceOutletOverrides(index=2, cycle_enabled=True),
            ],
            "index",
            [
                DeviceOutletOverrides(index=1, cycle_enabled=False),
                DeviceOutletOverrides(index=2, cycle_enabled=True),
            ],
        ),
        (
            [
                DeviceOutletOverrides(index=1, cycle_enabled=False),
            ],
            [
                DeviceOutletOverrides(index=1, cycle_enabled=True),
            ],
            "index",
            [
                DeviceOutletOverrides(index=1, cycle_enabled=True),
            ],
        ),
        (
            [
                DeviceOutletOverrides(index=3, cycle_enabled=False),
            ],
            [
                DeviceOutletOverrides(index=2, cycle_enabled=True),
            ],
            "index",
            [
                DeviceOutletOverrides(index=2, cycle_enabled=True),
                DeviceOutletOverrides(index=3, cycle_enabled=False),
            ],
        ),
        (
            [
                DeviceOutletOverrides(index=1, cycle_enabled=False),
                DeviceOutletOverrides(index=3, has_metering=False),
                DeviceOutletOverrides(index=4, relay_state=True),
            ],
            [
                DeviceOutletOverrides(index=2, cycle_enabled=True),
            ],
            "index",
            [
                DeviceOutletOverrides(index=1, cycle_enabled=False),
                DeviceOutletOverrides(index=2, cycle_enabled=True),
                DeviceOutletOverrides(index=3, has_metering=False),
                DeviceOutletOverrides(index=4, relay_state=True),
            ],
        ),
    ],
)
def test_merge_overrides(existing_overrides, new_overrides, index_attr, expected):
    """Verify the behavior of the _merge_overrides helper."""
    computed_overrides = _merge_overrides(existing_overrides, new_overrides, index_attr)
    assert expected == computed_overrides


# async def test_device_websocket(
#     unifi_controller: UnifiClient, new_ws_data_fn: Callable[[dict[str, Any]], None]
# ) -> None:
#     """Test controller managing devices."""
#     assert len(unifi_controller.devices._subscribers["*"]) == 2

#     unsub = unifi_controller.devices.subscribe(mock_callback := Mock())
#     assert len(unifi_controller.devices._subscribers["*"]) == 3
#     assert mock_callback.call_count == 0

#     # Add client from websocket
#     new_ws_data_fn(
#         {
#             "meta": {"message": MessageKey.DEVICE.value},
#             "data": [SWITCH_16_PORT_POE],
#         }
#     )
#     assert len(unifi_controller.devices.items()) == 1
#     assert len(unifi_controller.devices._subscribers["*"]) == 3

#     unsub()
#     assert len(unifi_controller.devices._subscribers["*"]) == 2


def test_enum_unknowns() -> None:
    """Validate enum unknown values."""
    assert DeviceState(999) == DeviceState.UNKNOWN


@pytest.mark.parametrize(
    ("method_name", "request_args", "api_request", "expected_error"),
    [
        (
            "send_cmd",
            {"device": TEST_DEVICE_1, "cmd": "test-cmd", "arg1": 1, "arg2": 2},
            {
                "method": "post",
                "endpoint": ApiEndpoint(path="/cmd/devmgr"),
                "data": {
                    "cmd": "test-cmd",
                    "mac": TEST_DEVICE_1.mac,
                    "arg1": 1,
                    "arg2": 2,
                },
            },
            None,
        ),
        (
            "power_cycle_port",
            {"device": TEST_DEVICE_1, "port_idx": 1},
            {
                "method": "post",
                "endpoint": ApiEndpoint(path="/cmd/devmgr"),
                "data": {
                    "cmd": "power-cycle",
                    "mac": TEST_DEVICE_1.mac,
                    "port_idx": 1,
                },
            },
            None,
        ),
        (
            "restart",
            {"device": TEST_DEVICE_1},
            {
                "method": "post",
                "endpoint": ApiEndpoint(path="/cmd/devmgr"),
                "data": {
                    "cmd": "restart",
                    "mac": TEST_DEVICE_1.mac,
                    "reboot_type": "soft",
                },
            },
            None,
        ),
        (
            "restart",
            {"device": TEST_DEVICE_1, "soft": True},
            {
                "method": "post",
                "endpoint": ApiEndpoint(path="/cmd/devmgr"),
                "data": {
                    "cmd": "restart",
                    "mac": TEST_DEVICE_1.mac,
                    "reboot_type": "soft",
                },
            },
            None,
        ),
        (
            "restart",
            {"device": TEST_DEVICE_1, "soft": False},
            {
                "method": "post",
                "endpoint": ApiEndpoint(path="/cmd/devmgr"),
                "data": {
                    "cmd": "restart",
                    "mac": TEST_DEVICE_1.mac,
                    "reboot_type": "hard",
                },
            },
            None,
        ),
        (
            "set_led_status",
            {
                "device": TEST_DEVICE_1,
                "brightness": -1,
            },
            None,
            ValueError,
        ),
        (
            "set_led_status",
            {
                "device": TEST_DEVICE_1,
                "color": "not a color",
            },
            None,
            ValueError,
        ),
        (
            "set_led_status",
            {
                "device": TEST_DEVICE_1,
                "brightness": 50,
            },
            {
                "method": "put",
                "endpoint": Devices.update_endpoint,
                "data": {"led_override": "on", "led_override_color_brightness": 50},
            },
            None,
        ),
        (
            "set_led_status",
            {
                "device": TEST_DEVICE_1,
                "color": "#ffffff",
            },
            {
                "method": "put",
                "endpoint": Devices.update_endpoint,
                "data": {"led_override": "on", "led_override_color": "#ffffff"},
            },
            None,
        ),
        (
            "set_outlet_overrides",
            {
                "device": TEST_DEVICE_1,
                "overrides": [DeviceOutletOverrides(index=1, relay_state=False)],
            },
            {
                "method": "put",
                "endpoint": Devices.update_endpoint,
                "data": {"outlet_overrides": [{"index": 1, "relay_state": False}]},
            },
            None,
        ),
        (
            "set_port_overrides",
            {
                "device": TEST_DEVICE_1,
                "overrides": [DevicePortOverrides(port_idx=1, poe_mode="auto")],
            },
            {
                "method": "put",
                "endpoint": Devices.update_endpoint,
                "data": {"port_overrides": [{"port_idx": 1, "poe_mode": "auto"}]},
            },
            None,
        ),
        (
            "upgrade",
            {"device": TEST_DEVICE_1},
            {
                "method": "post",
                "endpoint": ApiEndpoint(path="/cmd/devmgr"),
                "data": {
                    "cmd": "upgrade",
                    "mac": TEST_DEVICE_1.mac,
                },
            },
            None,
        ),
    ],
)
async def test_devices(
    method_name: str,
    request_args: dict[str, Any],
    api_request: dict[str, Any],
    expected_error: type[Exception] | None,
):
    """Test device interface methods."""
    await assert_handler_request(
        Devices, method_name, request_args, api_request, expected_error
    )


def test_device_id():
    """Confirm `id` property returns the `device_id` attribute."""
    assert TEST_DEVICE_1.device_id == TEST_DEVICE_1.id


@pytest.mark.parametrize(
    ("port", "expected_name"),
    [
        (Port(port_idx=1), "Port 1"),
        (Port(port_name="Ethernet 1", port_idx=1), "Ethernet 1"),
    ],
)
def test_port_name(port: Port, expected_name):
    """Verify behavior of the `name` property."""
    assert port.name == expected_name
