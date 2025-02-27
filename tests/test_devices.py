"""Test client configuration API.

pytest --cov-report term-missing --cov=aiounifi.devices tests/test_devices.py
"""

from collections.abc import Callable
from copy import deepcopy
from typing import Any
from unittest.mock import Mock

from aioresponses import aioresponses
import pytest

from aiounifi.controller import Controller
from aiounifi.models.api import ApiRequest
from aiounifi.models.device import (
    Device,
    DeviceListRequest,
    DeviceOutletOverrides,
    DevicePowerCyclePortRequest,
    DeviceRestartRequest,
    DeviceSetLedStatus,
    DeviceSetOutletCycleEnabledRequest,
    DeviceSetOutletRelayRequest,
    DeviceSetPoePortModeRequest,
    DeviceState,
    DeviceUpgradeRequest,
    Outlet,
    Port,
)
from aiounifi.models.message import MessageKey

from .fixtures import GATEWAY_USG3, SWITCH_16_PORT_POE, TEST_DEVICE_1, TEST_DEVICE_2

from tests.conftest import UnifiCalledWith


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
    ("request_cls", "kwargs", "want_method", "want_path", "want_data"),
    [
        (
            DeviceListRequest,
            {},
            "get",
            "/stat/device",
            None,
        ),
        (
            DevicePowerCyclePortRequest,
            {"mac": "00:01:02:03:04:05", "port_idx": 42},
            "post",
            "/cmd/devmgr",
            {
                "cmd": "power-cycle",
                "mac": "00:01:02:03:04:05",
                "port_idx": 42,
            },
        ),
        (
            DeviceRestartRequest,
            {"mac": "00:01:02:03:04:05", "soft": True},
            "post",
            "/cmd/devmgr",
            {
                "cmd": "restart",
                "mac": "00:01:02:03:04:05",
                "reboot_type": "soft",
            },
        ),
        (
            DeviceRestartRequest,
            {"mac": "00:01:02:03:04:05", "soft": False},
            "post",
            "/cmd/devmgr",
            {
                "cmd": "restart",
                "mac": "00:01:02:03:04:05",
                "reboot_type": "hard",
            },
        ),
        (
            DeviceUpgradeRequest,
            {"mac": "00:01:02:03:04:05"},
            "post",
            "/cmd/devmgr",
            {
                "cmd": "upgrade",
                "mac": "00:01:02:03:04:05",
            },
        ),
        (
            DeviceSetOutletRelayRequest,
            {
                "device": deepcopy(TEST_DEVICE_1),
                "outlet_idx": 1,
                "state": True,
            },
            "put",
            f"/rest/device/{TEST_DEVICE_1.id}",
            {
                "outlet_overrides": [
                    DeviceOutletOverrides(
                        index=1,
                        name=TEST_DEVICE_1.outlet_table[0].name,
                        relay_state=True,
                    ).to_json()
                ]
            },
        ),
        (
            DeviceSetOutletRelayRequest,
            {
                "device": deepcopy(TEST_DEVICE_1),
                "outlet_idx": 1,
                "state": False,
            },
            "put",
            f"/rest/device/{TEST_DEVICE_1.id}",
            {
                "outlet_overrides": [
                    DeviceOutletOverrides(
                        index=1,
                        name=TEST_DEVICE_1.outlet_table[0].name,
                        relay_state=False,
                    ).to_json()
                ]
            },
        ),
        (
            DeviceSetOutletRelayRequest,
            {
                "device": deepcopy(TEST_DEVICE_2),
                "outlet_idx": 2,
                "state": True,
            },
            "put",
            f"/rest/device/{TEST_DEVICE_2.id}",
            {
                "outlet_overrides": [
                    TEST_DEVICE_2.outlet_overrides[0].to_json(),
                    DeviceOutletOverrides(
                        index=2,
                        name=TEST_DEVICE_2.outlet_table[1].name,
                        relay_state=True,
                    ).to_json(),
                ]
            },
        ),
        (
            DeviceSetOutletRelayRequest,
            {
                "device": deepcopy(TEST_DEVICE_2),
                "outlet_idx": 2,
                "state": False,
            },
            "put",
            f"/rest/device/{TEST_DEVICE_2.id}",
            {
                "outlet_overrides": [
                    TEST_DEVICE_2.outlet_overrides[0].to_json(),
                    DeviceOutletOverrides(
                        index=2,
                        name=TEST_DEVICE_2.outlet_table[1].name,
                        relay_state=False,
                    ).to_json(),
                ]
            },
        ),
        (
            DeviceSetOutletCycleEnabledRequest,
            {"device": deepcopy(TEST_DEVICE_1), "outlet_idx": 1, "state": False},
            "put",
            f"/rest/device/{TEST_DEVICE_1.id}",
            {
                "outlet_overrides": [
                    DeviceOutletOverrides(
                        index=1,
                        name=TEST_DEVICE_1.outlet_table[0].name,
                        cycle_enabled=False,
                    ).to_json()
                ]
            },
        ),
        (
            DeviceSetOutletCycleEnabledRequest,
            {"device": deepcopy(TEST_DEVICE_1), "outlet_idx": 1, "state": True},
            "put",
            f"/rest/device/{TEST_DEVICE_1.id}",
            {
                "outlet_overrides": [
                    DeviceOutletOverrides(
                        index=1,
                        name=TEST_DEVICE_1.outlet_table[0].name,
                        cycle_enabled=True,
                    ).to_json()
                ]
            },
        ),
        (
            DeviceSetOutletCycleEnabledRequest,
            {"device": deepcopy(TEST_DEVICE_2), "outlet_idx": 2, "state": True},
            "put",
            f"/rest/device/{TEST_DEVICE_2.id}",
            {
                "outlet_overrides": [
                    TEST_DEVICE_2.outlet_overrides[0].to_json(),
                    DeviceOutletOverrides(
                        index=2,
                        name=TEST_DEVICE_2.outlet_table[1].name,
                        cycle_enabled=True,
                    ).to_json(),
                ]
            },
        ),
        (
            DeviceSetOutletCycleEnabledRequest,
            {"device": deepcopy(TEST_DEVICE_2), "outlet_idx": 2, "state": False},
            "put",
            f"/rest/device/{TEST_DEVICE_2.id}",
            {
                "outlet_overrides": [
                    TEST_DEVICE_2.outlet_overrides[0].to_json(),
                    DeviceOutletOverrides(
                        index=2,
                        name=TEST_DEVICE_2.outlet_table[1].name,
                        cycle_enabled=False,
                    ).to_json(),
                ]
            },
        ),
        # (DeviceSetPoePortModeRequest, {}, ""),
        # (DeviceSetLedStatus, {}, ""),
    ],
)
def test_api_requests(
    request_cls: type[ApiRequest],
    kwargs: dict[str, Any],
    want_method: str,
    want_path: str,
    want_data: dict[str, Any],
) -> None:
    """Verify the API requests generate the expected URLS."""
    request = request_cls(**kwargs)
    assert request.path == want_path
    assert request.method == want_method
    assert request.data == want_data


@pytest.mark.parametrize(
    ("device_payload", "api_request", "data", "command"),
    [
        (  # PoE port mode without existing override
            [
                {
                    "device_id": "01",
                    "mac": "0",
                    "port_overrides": [],
                    "port_table": [
                        {
                            "poe_mode": "Auto",
                            "name": "Port 1",
                            "port_idx": 1,
                        },
                    ],
                }
            ],
            DeviceSetPoePortModeRequest,
            {"port_idx": 1, "mode": "off"},
            {"port_overrides": [{"port_idx": 1, "poe_mode": "off"}]},
        ),
        (  # PoE port mode with portconf_id without existing override
            [
                {
                    "device_id": "01",
                    "mac": "0",
                    "port_overrides": [],
                    "port_table": [
                        {
                            "poe_mode": "Auto",
                            "name": "Port 1",
                            "port_idx": 1,
                            "portconf_id": "123",
                        },
                    ],
                }
            ],
            DeviceSetPoePortModeRequest,
            {"port_idx": 1, "mode": "off"},
            {
                "port_overrides": [
                    {"port_idx": 1, "poe_mode": "off", "portconf_id": "123"}
                ]
            },
        ),
        (  # PoE port mode with existing override
            [
                {
                    "device_id": "01",
                    "mac": "0",
                    "port_overrides": [{"port_idx": 1, "name": "Office"}],
                    "port_table": [
                        {
                            "poe_mode": "Auto",
                            "name": "Office",
                            "port_idx": 1,
                        },
                    ],
                }
            ],
            DeviceSetPoePortModeRequest,
            {"port_idx": 1, "mode": "off"},
            {"port_overrides": [{"port_idx": 1, "poe_mode": "off", "name": "Office"}]},
        ),
        (  # PoE multi target port mode with existing override
            [
                {
                    "device_id": "01",
                    "mac": "0",
                    "port_overrides": [{"port_idx": 1, "name": "Office"}],
                    "port_table": [
                        {
                            "poe_mode": "Auto",
                            "name": "Office",
                            "port_idx": 1,
                        },
                        {
                            "poe_mode": "Off",
                            "name": "Hallway",
                            "port_idx": 2,
                        },
                    ],
                }
            ],
            DeviceSetPoePortModeRequest,
            {"targets": [(1, "off"), (2, "auto")]},
            {
                "port_overrides": [
                    {"port_idx": 1, "poe_mode": "off", "name": "Office"},
                    {"port_idx": 2, "poe_mode": "auto"},
                ]
            },
        ),
    ],
)
@pytest.mark.usefixtures("_mock_endpoints")
async def test_sub_device_requests(
    mock_aioresponse: aioresponses,
    unifi_controller: Controller,
    unifi_called_with: UnifiCalledWith,
    api_request: type[DeviceSetOutletRelayRequest]
    | type[DeviceSetOutletCycleEnabledRequest]
    | type[DeviceSetPoePortModeRequest],
    data: dict[str, Any],
    command: dict[str, Any],
) -> None:
    """Test sub device (port/outlet) commands."""
    devices = unifi_controller.devices
    await devices.update()
    device = next(iter(devices.values()))
    mock_aioresponse.put("https://host:8443/api/s/default/rest/device/01", payload={})
    await unifi_controller.request(api_request(device, **data))
    assert unifi_called_with("put", "/api/s/default/rest/device/01", json=command)


@pytest.mark.parametrize(("device_payload"), [[SWITCH_16_PORT_POE]])
@pytest.mark.usefixtures("_mock_endpoints")
async def test_set_poe_request_raise_error(unifi_controller: Controller) -> None:
    """Test device class."""
    await unifi_controller.devices.update()
    device = next(iter(unifi_controller.devices.values()))
    with pytest.raises(AttributeError):
        DeviceSetPoePortModeRequest(device)


async def test_device_websocket(
    unifi_controller: Controller, new_ws_data_fn: Callable[[dict[str, Any]], None]
) -> None:
    """Test controller managing devices."""
    assert len(unifi_controller.devices._subscribers["*"]) == 2

    unsub = unifi_controller.devices.subscribe(mock_callback := Mock())
    assert len(unifi_controller.devices._subscribers["*"]) == 3
    assert mock_callback.call_count == 0

    # Add client from websocket
    new_ws_data_fn(
        {
            "meta": {"message": MessageKey.DEVICE.value},
            "data": [SWITCH_16_PORT_POE],
        }
    )
    assert len(unifi_controller.devices.items()) == 1
    assert len(unifi_controller.devices._subscribers["*"]) == 3

    unsub()
    assert len(unifi_controller.devices._subscribers["*"]) == 2


def test_enum_unknowns() -> None:
    """Validate enum unknown values."""
    assert DeviceState(999) == DeviceState.UNKNOWN


@pytest.mark.parametrize(
    ("device_payload", "data", "command"),
    [
        (
            [
                {
                    "device_id": "01",
                    "mac": "0",
                    "led_override": "on",
                    "led_override_color": "#0060fd",
                    "led_override_color_brightness": 100,
                    "hw_caps": 2562,
                }
            ],
            {"status": "off", "color": "#65e8a4", "brightness": 50},
            {
                "led_override": "off",
                "led_override_color": "#65e8a4",
                "led_override_color_brightness": 50,
            },
        ),
        (
            [
                {
                    "device_id": "01",
                    "mac": "0",
                    "led_override": "on",
                    "led_override_color": "#0060fd",
                    "led_override_color_brightness": 100,
                    "hw_caps": 2562,
                }
            ],
            {"status": "off", "brightness": 0},
            {
                "led_override": "off",
                "led_override_color_brightness": 0,
            },
        ),
        (
            [
                {
                    "device_id": "01",
                    "mac": "0",
                    "led_override": "on",
                    "led_override_color": "#0060fd",
                    "led_override_color_brightness": 100,
                    "hw_caps": 2562,
                }
            ],
            {"color": "#ffffff"},
            {
                "led_override": "on",
                "led_override_color": "#ffffff",
            },
        ),
    ],
)
@pytest.mark.usefixtures("_mock_endpoints")
async def test_led_status_request(
    mock_aioresponse: aioresponses,
    unifi_controller: Controller,
    unifi_called_with: UnifiCalledWith,
    device_payload: list[dict[str, Any]],
    data: dict[str, Any],
    command: dict[str, Any],
) -> None:
    """Tests LED status requests."""
    devices = unifi_controller.devices
    await devices.update()
    device = next(iter(devices.values()))
    mock_aioresponse.put(
        f"https://host:8443/api/s/default/rest/device/{device.id}", payload={}
    )
    api_request = DeviceSetLedStatus(device, **data)
    await unifi_controller.request(api_request)
    assert unifi_called_with(
        "put", f"/api/s/default/rest/device/{device.id}", json=command
    )


@pytest.mark.parametrize(
    ("device_payload", "data"),
    [
        (
            [
                {
                    "device_id": "01",
                    "mac": "0",
                    "led_override": "on",
                    "led_override_color": "#0060fd",
                    "led_override_color_brightness": 100,
                    "hw_caps": 2562,
                }
            ],
            {"status": "off", "color": "foobar", "brightness": 100},
        ),
        (
            [
                {
                    "device_id": "01",
                    "mac": "0",
                    "led_override": "on",
                    "led_override_color": "#0060fd",
                    "led_override_color_brightness": 100,
                    "hw_caps": 2562,
                }
            ],
            {"status": "off", "brightness": -99},
        ),
    ],
)
@pytest.mark.usefixtures("_mock_endpoints")
async def test_led_status_request_exception(
    mock_aioresponse: aioresponses,
    unifi_controller: Controller,
    unifi_called_with: UnifiCalledWith,
    device_payload: list[dict[str, Any]],
    data: dict[str, Any],
) -> None:
    """Tests LED status requests raise AttributeError."""
    devices = unifi_controller.devices
    await devices.update()
    device = next(iter(devices.values()))
    mock_aioresponse.put(
        f"https://host:8443/api/s/default/rest/device/{device.id}", payload={}
    )
    with pytest.raises(AttributeError):
        DeviceSetLedStatus(device, **data)


@pytest.mark.parametrize(("device_payload"), [[GATEWAY_USG3]])
@pytest.mark.usefixtures("_mock_endpoints")
async def test_update_stats(unifi_controller: Controller) -> None:
    """Test device class uptime stats."""
    await unifi_controller.devices.update()
    device = next(iter(unifi_controller.devices.values()))

    assert device.uptime_stats is not None
    assert len(device.uptime_stats.WAN.monitors) == 3
    assert len(device.uptime_stats.WAN2.monitors) == 3

    assert device.uptime_stats.WAN.monitors[0].availability == 100.0
    assert device.uptime_stats.WAN.monitors[0].latency_average == 5
    assert device.uptime_stats.WAN.monitors[0].target == "www.microsoft.com"
    assert device.uptime_stats.WAN.monitors[0].type == "icmp"


@pytest.mark.parametrize(("device_payload"), [[GATEWAY_USG3]])
@pytest.mark.usefixtures("_mock_endpoints")
async def test_storage(unifi_controller: Controller) -> None:
    """Test device class storage."""
    await unifi_controller.devices.update()
    device = next(iter(unifi_controller.devices.values()))

    assert device.storage is not None
    assert len(device.storage) == 2

    assert device.storage[0].mount_point == "/persistent"
    assert device.storage[0].name == "Backup"
    assert device.storage[0].size == 2040373248
    assert device.storage[0].type == "eMMC"
    assert device.storage[0].used == 148353024


@pytest.mark.parametrize(("device_payload"), [[GATEWAY_USG3]])
@pytest.mark.usefixtures("_mock_endpoints")
async def test_temperatures(unifi_controller: Controller) -> None:
    """Test device class temperatures."""
    await unifi_controller.devices.update()
    device = next(iter(unifi_controller.devices.values()))

    assert device.temperatures is not None
    assert len(device.temperatures) == 3

    assert device.temperatures[0].name == "CPU"
    assert device.temperatures[0].type == "cpu"
    assert device.temperatures[0].value == 66.0
