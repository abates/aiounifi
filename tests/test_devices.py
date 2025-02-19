"""Test client configuration API.

pytest --cov-report term-missing --cov=aiounifi.devices tests/test_devices.py
"""

from collections.abc import Callable
from typing import Any
from unittest.mock import Mock

from aioresponses import aioresponses
import pytest

from aiounifi.controller import Controller
from aiounifi.models.device import (
    DeviceLldpTable,
    DeviceOutletOverrides,
    DevicePortOverrides,
    DevicePowerCyclePortRequest,
    DeviceRestartRequest,
    DeviceSetLedStatus,
    DeviceSetOutletCycleEnabledRequest,
    DeviceSetOutletRelayRequest,
    DeviceSetPoePortModeRequest,
    DeviceSpeedtestStatus,
    DeviceState,
    DeviceSysStats,
    DeviceSystemStats,
    DeviceUpgradeRequest,
    DeviceUplink,
    DeviceUptimeStats,
    DeviceUptimeStatsWan,
    DeviceUptimeStatsWanMonitor,
    DeviceWlanOverrides,
    Outlet,
    Port,
)
from aiounifi.models.message import MessageKey

from .fixtures import (
    ACCESS_POINT_AC_PRO,
    GATEWAY_USG3,
    PDU_PRO,
    PLUG_UP1,
    STRIP_UP6,
    SWITCH_16_PORT_POE,
)

from tests.conftest import UnifiCalledWith

test_data = [
    ([{"mac": "0", "disabled": True}], {"mac": "0", "disabled": True}),
    (
        [ACCESS_POINT_AC_PRO],
        {
            "board_revision": 21,
            "considered_lost_at": 1588175837,
            "disabled": False,
            "id": "235678987654345678",
            "ip": "192.168.0.4",
            "downlink_table": [],
            "fan_level": None,
            "has_fan": False,
            "last_seen": 1588175726,
            "led_override": "on",
            "lldp_table": [],
            "mac": "80:2a:a8:00:01:02",
            "model": "U7PG2",
            "name": "ACCESS POINT AC PRO",
            "next_heartbeat_at": 1588175763,
            "overheating": False,
            "port_overrides": [],
            "port_table": [
                Port.from_json(port_table)
                for port_table in ACCESS_POINT_AC_PRO["port_table"]
            ],
            "speedtest_status": None,
            "state": 1,
            "sys_stats": DeviceSysStats(
                loadavg_1="0.15",
                loadavg_15="0.02",
                loadavg_5="0.08",
                mem_buffer=0,
                mem_total=128622592,
                mem_used=63606784,
            ),
            "type": "uap",
            "version": "4.0.69.10871",
            "upgradable": True,
            "upgrade_to_firmware": "4.0.80.10875",
            "uplink": DeviceUplink.from_json(ACCESS_POINT_AC_PRO["uplink"]),
            "uplink_depth": None,
            "user_num_sta": 12,
            "wlan_overrides": [
                DeviceWlanOverrides(
                    name="My5GHzSSID1",
                    radio="na",
                    radio_name="wifi1",
                    wlan_id="012345678910111213141516",
                ),
            ],
        },
    ),
    (
        [GATEWAY_USG3],
        {
            "board_revision": 16,
            "considered_lost_at": 1588175842,
            "disabled": False,
            "general_temperature": None,
            "has_temperature": False,
            "id": "235678987654345678",
            "ip": "1.2.3.4",
            "downlink_table": [],
            "fan_level": None,
            "has_fan": False,
            "last_seen": 1588175740,
            "lldp_table": [],
            "mac": "78:8a:20:33:44:55",
            "model": "UGW3",
            "name": "USG",
            "next_heartbeat_at": 1588175774,
            "overheating": False,
            "port_overrides": [],
            "port_table": [
                Port.from_json(port_table) for port_table in GATEWAY_USG3["port_table"]
            ],
            "state": 1,
            "sys_stats": DeviceSysStats(
                loadavg_1="0.03",
                loadavg_15="0.08",
                loadavg_5="0.07",
                mem_buffer=57561088,
                mem_total=507412480,
                mem_used=293453824,
            ),
            "system_stats": DeviceSystemStats("0", "25", "3971505"),
            "type": "ugw",
            "version": "4.4.44.5213844",
            "upgradable": True,
            "upgrade_to_firmware": "4.4.50.5272448",
            "uplink": DeviceUplink.from_json(GATEWAY_USG3["uplink"]),
            "uplink_depth": None,
            "uptime": 3971869,
            "uptime_stats": DeviceUptimeStats(
                WAN=DeviceUptimeStatsWan(
                    monitors=[
                        DeviceUptimeStatsWanMonitor(
                            availability=100.0,
                            latency_average=5,
                            target="www.microsoft.com",
                            type="icmp",
                        ),
                        DeviceUptimeStatsWanMonitor(
                            availability=100.0,
                            latency_average=7,
                            target="google.com",
                            type="icmp",
                        ),
                        DeviceUptimeStatsWanMonitor(
                            availability=100.0,
                            latency_average=5,
                            target="1.1.1.1",
                            type="icmp",
                        ),
                    ]
                ),
                WAN2=DeviceUptimeStatsWan(
                    monitors=[
                        DeviceUptimeStatsWanMonitor(
                            availability=0.0,
                            target="www.microsoft.com",
                            type="icmp",
                        ),
                        DeviceUptimeStatsWanMonitor(
                            availability=0.0, target="google.com", type="icmp"
                        ),
                        DeviceUptimeStatsWanMonitor(
                            availability=0.0, target="1.1.1.1", type="icmp"
                        ),
                    ]
                ),
            ),
            "user_num_sta": 20,
            "wlan_overrides": [],
            "speedtest_status": DeviceSpeedtestStatus.from_json(
                GATEWAY_USG3["speedtest-status"]
            ),
        },
    ),
    (
        [PLUG_UP1],
        {
            "board_revision": 2,
            "downlink_table": [],
            "id": "600c8356942a6ade50707b56",
            "ip": "192.168.0.189",
            "has_fan": False,
            "has_temperature": False,
            "general_temperature": None,
            "last_seen": 1642055273,
            "led_override": "on",
            "led_override_color": "#0000ff",
            "led_override_color_brightness": 100,
            "lldp_table": [],
            "mac": "fc:ec:da:76:4f:5f",
            "model": "UP1",
            "name": "Plug",
            "next_interval": 40,
            "outlet_table": [
                Outlet(
                    index=1,
                    has_relay=True,
                    has_metering=False,
                    relay_state=False,
                    name="Outlet 1",
                )
            ],
            "outlet_overrides": [],
            "port_table": [],
            "state": 1,
            "sys_stats": DeviceSysStats(mem_total=98304, mem_used=87736),
            "system_stats": DeviceSystemStats("", "", ""),
            "type": "uap",
            "version": "2.2.1.511",
            "upgradable": False,
            "uplink": DeviceUplink.from_json(PLUG_UP1["uplink"]),
            "uptime": 376083,
        },
    ),
    (
        [STRIP_UP6],
        {
            "board_revision": 5,
            "downlink_table": [],
            "general_temperature": None,
            "has_temperature": False,
            "id": "61eb1a75942a6a859b45d2bc",
            "ip": "192.168.0.138",
            "has_fan": False,
            "last_seen": 1642800247,
            "lldp_table": [],
            "mac": "78:45:58:fc:16:7d",
            "model": "UP6",
            "name": "",
            "next_interval": 41,
            "outlet_table": [
                Outlet(
                    index=1,
                    has_relay=True,
                    has_metering=False,
                    relay_state=False,
                    cycle_enabled=False,
                    name="Outlet 1",
                ),
                Outlet(
                    index=2,
                    has_relay=True,
                    has_metering=False,
                    relay_state=False,
                    cycle_enabled=False,
                    name="Outlet 2",
                ),
                Outlet(
                    index=3,
                    has_relay=True,
                    has_metering=False,
                    relay_state=True,
                    cycle_enabled=False,
                    name="Outlet 3",
                ),
                Outlet(
                    index=4,
                    has_relay=True,
                    has_metering=False,
                    relay_state=True,
                    cycle_enabled=True,
                    name="Outlet 4",
                ),
                Outlet(
                    index=5,
                    has_relay=True,
                    has_metering=False,
                    relay_state=False,
                    cycle_enabled=False,
                    name="Outlet 5",
                ),
                Outlet(
                    index=6,
                    has_relay=True,
                    has_metering=False,
                    relay_state=False,
                    cycle_enabled=False,
                    name="Outlet 6",
                ),
                Outlet(
                    index=7,
                    has_relay=True,
                    has_metering=False,
                    relay_state=False,
                    cycle_enabled=False,
                    name="USB Outlets",
                ),
            ],
            "outlet_overrides": [
                DeviceOutletOverrides(
                    index=1,
                    name="Outlet 1",
                    cycle_enabled=False,
                    relay_state=False,
                ),
                DeviceOutletOverrides(
                    index=2,
                    name="Outlet 2",
                    cycle_enabled=False,
                    relay_state=False,
                ),
                DeviceOutletOverrides(
                    index=3,
                    name="Outlet 3",
                    cycle_enabled=False,
                    relay_state=True,
                ),
                DeviceOutletOverrides(
                    index=4,
                    name="Outlet 4",
                    cycle_enabled=True,
                    relay_state=True,
                ),
                DeviceOutletOverrides(
                    index=5,
                    name="Outlet 5",
                    cycle_enabled=False,
                    relay_state=False,
                ),
                DeviceOutletOverrides(
                    index=6,
                    name="Outlet 6",
                    cycle_enabled=False,
                    relay_state=False,
                ),
                DeviceOutletOverrides(
                    index=7,
                    name="USB Outlets",
                    cycle_enabled=False,
                    relay_state=False,
                ),
            ],
            "port_table": [],
            "state": 1,
            "sys_stats": DeviceSysStats(mem_total=98304, mem_used=88056),
            "system_stats": DeviceSystemStats("", "", ""),
            "type": "uap",
            "version": "2.2.1.511",
            "upgradable": False,
            "uplink": DeviceUplink.from_json(STRIP_UP6["uplink"]),
            "uptime": 2370,
        },
    ),
    (
        [PDU_PRO],
        {
            "board_revision": 1,
            "downlink_table": [],
            "general_temperature": None,
            "has_temperature": False,
            "id": "61e4a1e60bbb2d53aeb430ea",
            "ip": "192.168.1.66",
            "has_fan": False,
            "last_seen": 1643721168,
            "lldp_table": [
                DeviceLldpTable(
                    chassis_id="00:00:00:00:00:83",
                    chassis_id_subtype="mac",
                    is_wired=True,
                    local_port_idx=1,
                    local_port_name="eth0",
                    port_id="local Port 1",
                )
            ],
            "mac": "00:00:00:00:00:84",
            "model": "USPPDUP",
            "name": "Main Server Cabinet PDU",
            "next_interval": 56,
            "outlet_ac_power_budget": "1875.000",
            "outlet_ac_power_consumption": "307.741",
            "outlet_table": [
                Outlet(
                    index=1,
                    relay_state=True,
                    cycle_enabled=False,
                    name="USB Outlet 1",
                    caps=1,
                ),
                Outlet(
                    index=2,
                    relay_state=False,
                    cycle_enabled=False,
                    name="USB Outlet 2",
                    caps=1,
                ),
                Outlet(
                    index=3,
                    relay_state=True,
                    cycle_enabled=False,
                    name="USB Outlet 3",
                    caps=1,
                ),
                Outlet(
                    index=4,
                    relay_state=False,
                    cycle_enabled=False,
                    name="USB Outlet 4",
                    caps=1,
                ),
                Outlet(
                    index=5,
                    relay_state=True,
                    name="Console",
                    caps=3,
                    voltage="118.566",
                    current="0.061",
                    power="3.815",
                    power_factor="0.527",
                ),
                Outlet(
                    index=6,
                    relay_state=True,
                    name="UDM Pro",
                    caps=3,
                    voltage="118.566",
                    current="0.248",
                    power="14.351",
                    power_factor="0.488",
                ),
                Outlet(
                    index=7,
                    relay_state=True,
                    name="Unraid",
                    caps=3,
                    voltage="118.566",
                    current="1.454",
                    power="169.900",
                    power_factor="0.985",
                ),
                Outlet(
                    index=8,
                    relay_state=True,
                    caps=3,
                    voltage="118.566",
                    current="0.000",
                    power="0.000",
                    power_factor="0.000",
                    name="Outlet 8",
                ),
                Outlet(
                    index=9,
                    relay_state=True,
                    caps=3,
                    voltage="118.566",
                    current="0.000",
                    power="0.000",
                    power_factor="0.000",
                    name="Outlet 9",
                ),
                Outlet(
                    index=10,
                    relay_state=True,
                    caps=3,
                    voltage="118.566",
                    current="0.000",
                    power="0.000",
                    power_factor="0.000",
                    name="Outlet 10",
                ),
                Outlet(
                    index=11,
                    relay_state=False,
                    caps=3,
                    voltage="118.566",
                    current="0.000",
                    power="0.000",
                    power_factor="0.000",
                    name="Outlet 11",
                ),
                Outlet(
                    index=12,
                    relay_state=True,
                    caps=3,
                    voltage="118.566",
                    current="0.000",
                    power="0.000",
                    power_factor="0.000",
                    name="Outlet 12",
                ),
                Outlet(
                    index=13,
                    relay_state=True,
                    caps=3,
                    voltage="118.566",
                    current="0.000",
                    power="0.000",
                    power_factor="0.000",
                    name="Outlet 13",
                ),
                Outlet(
                    index=14,
                    relay_state=True,
                    caps=3,
                    voltage="118.566",
                    current="0.000",
                    power="0.000",
                    power_factor="0.000",
                    name="Outlet 14",
                ),
                Outlet(
                    index=15,
                    relay_state=True,
                    caps=3,
                    voltage="118.566",
                    current="0.127",
                    power="9.394",
                    power_factor="0.623",
                    name="Outlet 15",
                ),
                Outlet(
                    index=16,
                    relay_state=True,
                    name="UNVR Pro",
                    caps=3,
                    voltage="118.566",
                    current="0.278",
                    power="31.992",
                    power_factor="0.970",
                ),
                Outlet(
                    index=17,
                    relay_state=True,
                    caps=3,
                    voltage="118.566",
                    current="0.000",
                    power="0.000",
                    power_factor="0.000",
                    name="Outlet 17",
                ),
                Outlet(
                    index=18,
                    relay_state=True,
                    name="Home Assistant",
                    caps=3,
                    voltage="118.566",
                    current="0.328",
                    power="21.529",
                    power_factor="0.553",
                ),
                Outlet(
                    index=19,
                    relay_state=True,
                    name="Server Cabinet Switch",
                    caps=3,
                    voltage="118.566",
                    current="0.495",
                    power="56.760",
                    power_factor="0.967",
                ),
                Outlet(
                    index=20,
                    relay_state=True,
                    name="Rear Cabinet Lights",
                    caps=3,
                    voltage="118.566",
                    current="0.000",
                    power="0.000",
                    power_factor="0.000",
                ),
            ],
            "outlet_overrides": [
                DeviceOutletOverrides(
                    index=1,
                    name="USB Outlet 1",
                    cycle_enabled=False,
                    relay_state=False,
                ),
                DeviceOutletOverrides(
                    index=2,
                    name="USB Outlet 2",
                    cycle_enabled=False,
                    relay_state=False,
                ),
                DeviceOutletOverrides(
                    index=3,
                    name="USB Outlet 3",
                    cycle_enabled=False,
                    relay_state=False,
                ),
                DeviceOutletOverrides(
                    index=4,
                    name="USB Outlet 4",
                    cycle_enabled=False,
                    relay_state=False,
                ),
                DeviceOutletOverrides(index=5, name="Console", relay_state=True),
                DeviceOutletOverrides(index=6, name="UDM Pro", relay_state=True),
                DeviceOutletOverrides(index=7, name="Unraid", relay_state=True),
                DeviceOutletOverrides(index=8, relay_state=True),
                DeviceOutletOverrides(index=9, relay_state=True),
                DeviceOutletOverrides(index=10, relay_state=True),
                DeviceOutletOverrides(index=11, relay_state=True),
                DeviceOutletOverrides(index=12, relay_state=True),
                DeviceOutletOverrides(index=13, relay_state=True),
                DeviceOutletOverrides(index=14, relay_state=True),
                DeviceOutletOverrides(index=15, relay_state=True),
                DeviceOutletOverrides(index=16, name="UNVR Pro", relay_state=True),
                DeviceOutletOverrides(index=17, relay_state=True),
                DeviceOutletOverrides(
                    index=18, name="Home Assistant", relay_state=True
                ),
                DeviceOutletOverrides(
                    index=19, name="Server Cabinet Switch", relay_state=True
                ),
                DeviceOutletOverrides(
                    index=20, name="Rear Cabinet Lights", relay_state=True
                ),
            ],
            "port_table": [
                Port(
                    port_idx=1,
                    media="FE",
                    port_poe=False,
                    poe_caps=0,
                    speed_caps=1048591,
                    op_mode="switch",
                    portconf_id="5fc7fb23c3da2e039ebeea97",
                    autoneg=False,
                    enable=True,
                    flowctrl_rx=False,
                    flowctrl_tx=False,
                    full_duplex=True,
                    is_uplink=True,
                    jumbo=False,
                    mac_table=[],
                    rx_broadcast=0,
                    rx_bytes=538000102,
                    rx_dropped=2,
                    rx_errors=0,
                    rx_multicast=0,
                    rx_packets=3943979,
                    satisfaction=90,
                    satisfaction_reason=1,
                    speed=100,
                    stp_pathcost=0,
                    stp_state="disabled",
                    tx_broadcast=0,
                    tx_bytes=114523726,
                    tx_dropped=0,
                    tx_errors=0,
                    tx_multicast=0,
                    tx_packets=670312,
                    up=True,
                    tx_bytes_r=82,
                    rx_bytes_r=1510,
                    bytes_r=1592,
                    port_name="Port 1",
                    masked=False,
                    aggregated_by=False,
                )
            ],
            "state": 1,
            "sys_stats": DeviceSysStats(
                loadavg_1="0.08",
                loadavg_15="0.01",
                loadavg_5="0.02",
                mem_buffer=0,
                mem_total=61792256,
                mem_used=18235392,
            ),
            "system_stats": DeviceSystemStats("1.1", "29.5", "1347471"),
            "type": "usw",
            "version": "5.76.7.13442",
            "upgradable": False,
            "uplink": DeviceUplink.from_json(PDU_PRO["uplink"]),
            "uptime": 1347471,
        },
    ),
    (
        [SWITCH_16_PORT_POE],
        {
            "board_revision": 9,
            "considered_lost_at": 1588175821,
            "disabled": False,
            "general_temperature": 56,
            "has_temperature": True,
            "id": "235678987654345678",
            "ip": "192.168.0.57",
            "downlink_table": [],
            "fan_level": 0,
            "has_fan": True,
            "last_seen": 1588175722,
            "lldp_table": [],
            "mac": "fc:ec:da:11:22:33",
            "model": "US16P150",
            "name": "Switch 16",
            "next_interval": 23,
            "next_heartbeat_at": 1588175755,
            "overheating": False,
            "port_overrides": [
                DevicePortOverrides(
                    poe_mode="auto",
                    portconf_id="5e1b309714bd614afd3d11a7",
                    port_security_mac_address=[],
                    autoneg=True,
                    stp_port_mode=True,
                ),
                DevicePortOverrides(
                    poe_mode="off",
                    port_idx=3,
                    portconf_id="5a32aa4ee4babd4452422ddd22222",
                ),
                DevicePortOverrides(
                    poe_mode="auto",
                    port_idx=4,
                    portconf_id="5a32aa4ee4babd4452422ddd22222",
                ),
                DevicePortOverrides(
                    poe_mode="auto",
                    port_idx=16,
                    portconf_id="5a32aa4ee4babd4452422ddd22222",
                ),
            ],
            "port_table": [
                Port.from_json(table) for table in SWITCH_16_PORT_POE["port_table"]
            ],
            "state": 1,
            "sys_stats": DeviceSysStats(
                loadavg_1="2.82",
                loadavg_15="2.81",
                loadavg_5="2.80",
                mem_buffer=0,
                mem_total=262402048,
                mem_used=129331200,
            ),
            "system_stats": DeviceSystemStats("100.0", "49.3", "3971865"),
            "type": "usw",
            "version": "4.0.66.10832",
            "upgradable": True,
            "upgrade_to_firmware": "4.0.80.10875",
            "uplink": DeviceUplink.from_json(SWITCH_16_PORT_POE["uplink"]),
            "uplink_depth": 2,
            "uptime": 3971865,
            "user_num_sta": 4,
            "wlan_overrides": [],
        },
    ),
]


@pytest.mark.parametrize(("device_payload", "reference_data"), test_data)
@pytest.mark.usefixtures("_mock_endpoints")
async def test_device(
    unifi_controller: Controller, reference_data: dict[str, Any]
) -> None:
    """Test device class."""
    devices = unifi_controller.devices
    await devices.update()
    assert len(devices.items()) == 1

    device = next(iter(devices.values()))
    for key, value in reference_data.items():
        assert getattr(device, key) == value
    assert repr(device) == f"<Device {device.name}: {device.mac}>"


@pytest.mark.parametrize(
    ("method", "mac", "command"),
    [("upgrade", "0", {"mac": "0", "cmd": "upgrade"})],
)
async def test_device_commands(
    mock_aioresponse: aioresponses,
    unifi_controller: Controller,
    unifi_called_with: UnifiCalledWith,
    method: str,
    mac: str,
    command: dict[str, Any],
) -> None:
    """Test device commands."""
    mock_aioresponse.post("https://host:8443/api/s/default/cmd/devmgr", payload={})
    class_command = getattr(unifi_controller.devices, method)
    await class_command(mac)
    assert unifi_called_with("post", "/api/s/default/cmd/devmgr", json=command)


@pytest.mark.parametrize(
    ("api_request", "data", "command"),
    [
        (
            DeviceRestartRequest,
            {"mac": "0", "soft": True},
            {"mac": "0", "cmd": "restart", "reboot_type": "soft"},
        ),
        (
            DeviceRestartRequest,
            {"mac": "0", "soft": False},
            {"mac": "0", "cmd": "restart", "reboot_type": "hard"},
        ),
        (
            DeviceUpgradeRequest,
            {"mac": "0"},
            {"mac": "0", "cmd": "upgrade"},
        ),
        (
            DevicePowerCyclePortRequest,
            {"mac": "0", "port_idx": 1},
            {"mac": "0", "port_idx": 1, "cmd": "power-cycle"},
        ),
    ],
)
async def test_device_requests(
    mock_aioresponse: aioresponses,
    unifi_controller: Controller,
    unifi_called_with: UnifiCalledWith,
    api_request: DeviceRestartRequest
    | DeviceUpgradeRequest
    | DevicePowerCyclePortRequest,
    data: dict[str, Any],
    command: dict[str, Any],
) -> None:
    """Test device commands."""
    mock_aioresponse.post("https://host:8443/api/s/default/cmd/devmgr", payload={})
    await unifi_controller.request(api_request.create(**data))
    assert unifi_called_with("post", "/api/s/default/cmd/devmgr", json=command)


@pytest.mark.parametrize(
    ("device_payload", "api_request", "data", "command"),
    [
        (  # Outlet set relay without existing override
            [
                {
                    "device_id": "01",
                    "mac": "0",
                    "outlet_overrides": [],
                    "outlet_table": [
                        {
                            "index": 1,
                            "relay_state": True,
                            "cycle_enabled": False,
                            "name": "USB Outlet 1",
                            "caps": 1,
                        },
                    ],
                }
            ],
            DeviceSetOutletRelayRequest,
            {"outlet_idx": 1, "state": True},
            {
                "outlet_overrides": [
                    {"index": 1, "name": "USB Outlet 1", "relay_state": True}
                ]
            },
        ),
        (  # Outlet set relay with existing override
            [
                {
                    "device_id": "01",
                    "mac": "0",
                    "outlet_overrides": [{"index": 2}],
                    "outlet_table": [
                        {
                            "index": 2,
                            "relay_state": True,
                            "cycle_enabled": False,
                            "name": "USB Outlet 1",
                            "caps": 1,
                        },
                    ],
                }
            ],
            DeviceSetOutletRelayRequest,
            {"outlet_idx": 2, "state": False},
            {"outlet_overrides": [{"index": 2, "relay_state": False}]},
        ),
        (  # Outlet outlet cycle without existing override
            [
                {
                    "device_id": "01",
                    "mac": "0",
                    "outlet_overrides": [],
                    "outlet_table": [
                        {
                            "index": 1,
                            "relay_state": True,
                            "cycle_enabled": False,
                            "name": "USB Outlet 1",
                            "caps": 1,
                        },
                    ],
                }
            ],
            DeviceSetOutletCycleEnabledRequest,
            {"outlet_idx": 1, "state": True},
            {
                "outlet_overrides": [
                    {"index": 1, "name": "USB Outlet 1", "cycle_enabled": True}
                ]
            },
        ),
        (  # Outlet outlet cycle with existing override
            [
                {
                    "device_id": "01",
                    "mac": "0",
                    "outlet_overrides": [{"index": 2}],
                    "outlet_table": [
                        {
                            "index": 2,
                            "relay_state": True,
                            "cycle_enabled": False,
                            "name": "USB Outlet 1",
                            "caps": 1,
                        },
                    ],
                }
            ],
            DeviceSetOutletCycleEnabledRequest,
            {"outlet_idx": 2, "state": False},
            {"outlet_overrides": [{"index": 2, "cycle_enabled": False}]},
        ),
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
    api_request: DeviceSetOutletRelayRequest
    | DeviceSetOutletCycleEnabledRequest
    | DeviceSetPoePortModeRequest,
    data: dict[str, Any],
    command: dict[str, Any],
) -> None:
    """Test sub device (port/outlet) commands."""
    devices = unifi_controller.devices
    await devices.update()
    device = next(iter(devices.values()))
    mock_aioresponse.put("https://host:8443/api/s/default/rest/device/01", payload={})
    await unifi_controller.request(api_request.create(device, **data))
    assert unifi_called_with("put", "/api/s/default/rest/device/01", json=command)


@pytest.mark.parametrize(("device_payload"), [[SWITCH_16_PORT_POE]])
@pytest.mark.usefixtures("_mock_endpoints")
async def test_set_poe_request_raise_error(unifi_controller: Controller) -> None:
    """Test device class."""
    await unifi_controller.devices.update()
    device = next(iter(unifi_controller.devices.values()))
    with pytest.raises(AttributeError):
        DeviceSetPoePortModeRequest.create(device)


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
    api_request = DeviceSetLedStatus.create(device, **data)
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
        DeviceSetLedStatus.create(device, **data)


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
