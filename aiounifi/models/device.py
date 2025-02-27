"""UniFi devices are network infrastructure."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
import enum
import logging
import re

from .api import ApiItem, ApiRequest, json_field

LOGGER = logging.getLogger(__name__)


@dataclass
class DeviceAntennaTable(ApiItem):
    """Device antenna table type definition."""

    default: bool = False
    id: int = 0
    name: str = ""
    wifi0_gain: int = 0
    wifi1_gain: int = 0


@dataclass
class DeviceConfigNetwork(ApiItem):
    """Device config network type definition."""

    ip: str = ""
    type: str = ""


@dataclass
class DeviceEthernetOverrides(ApiItem):
    """Device ethernet overrides type definition."""

    ifname: str = ""
    networkgroup: str = ""


@dataclass
class DeviceEthernetTable(ApiItem):
    """Device ethernet table type definition."""

    mac: str = ""
    name: str = ""
    num_port: int = 0


@dataclass
class DeviceLastUplink(ApiItem):
    """Device last uplink type definition."""

    port_idx: int = 0
    type: str = ""
    uplink_mac: str = ""
    uplink_device_name: str = ""
    uplink_remote_port: int = 0


@dataclass
class DeviceLldpTable(ApiItem):
    """Device LLDP table type definition."""

    chassis_id: str = ""
    chassis_id_subtype: str = ""
    is_wired: bool = False
    local_port_idx: int = 0
    local_port_name: str = ""
    port_id: str = ""


@dataclass
class DeviceNetworkTable(ApiItem):
    """Device network table type definition."""

    _id: str = ""
    attr_hidden_id: str = ""
    attr_no_delete: bool = False
    dhcp_relay_enabled: bool = False
    dhcpd_dns_1: str = ""
    dhcpd_dns_enabled: bool = False
    dhcpd_enabled: bool = False
    dhcpd_gateway_enabled: bool = False
    dhcpd_leasetime: int = 0
    dhcpd_start: str = ""
    dhcpd_stop: str = ""
    dhcpd_time_offset_enabled: bool = False
    dhcpd_unifi_controller: str = ""
    domain_name: str = ""
    enabled: bool = False
    ip: str = ""
    ip_subnet: str = ""
    is_guest: bool = False
    is_nat: bool = False
    lte_lan_enabled: bool = False
    mac: str = ""
    name: str = ""
    networkgroup: str = ""
    num_sta: int = 0
    purpose: str = ""
    rx_bytes: int = 0
    rx_packets: int = 0
    site_id: str = ""
    tx_bytes: int = 0
    tx_packets: int = 0
    up: str = ""
    vlan_enabled: bool = False


@dataclass
class DeviceOutletOverrides(ApiItem):
    """Device outlet overrides type definition."""

    cycle_enabled: bool | None = None
    index: int = 0
    has_relay: bool | None = None
    has_metering: bool | None = None
    name: str | None = None
    relay_state: bool | None = None


@dataclass
class Outlet(ApiItem):
    """Device outlet table type definition."""

    caps: int | None = json_field("outlet_caps", default=None)
    current: str | None = json_field("outlet_current", default=None)
    cycle_enabled: bool | None = None
    has_relay: bool | None = None
    has_metering: bool | None = None
    index: int = 0
    name: str = ""
    power: str | None = json_field("outlet_power", default=None)
    power_factor: str | None = json_field("outlet_power_factor", default=None)
    relay_state: bool | None = None
    voltage: str | None = json_field("outlet_voltage", default=None)

    def __repr__(self) -> str:
        """Return the representation."""
        return f"<{self.name}: relay state {self.relay_state}>"


@dataclass
class DevicePortOverrides(ApiItem):
    """Device port overrides type definition."""

    name: str | None = None
    poe_mode: str = ""
    port_idx: int = 0
    portconf_id: str | None = None
    port_security_mac_address: list[str] | None = None
    autoneg: bool | None = None
    stp_port_mode: bool | None = None


@dataclass
class DevicePortTableLldpTable(ApiItem):
    """Device port table mac table type definition."""

    lldp_chassis_id: str = ""
    lldp_port_id: str = ""
    lldp_system_name: str = ""


@dataclass
class DevicePortTableMacTable(ApiItem):
    """Device port table mac table type definition."""

    age: int = 0
    mac: str = ""
    static: bool = False
    uptime: int = 0
    vlan: int = 0


@dataclass
class DevicePortTablePortDelta(ApiItem):
    """Device port table port delta type definition."""

    rx_bytes: int = 0
    rx_packets: int = 0
    time_delta: int = 0
    time_delta_activity: int = 0
    tx_bytes: int = 0
    tx_packets: int = 0


@dataclass
class Port(ApiItem):
    """Device port table type definition."""

    aggregated_by: bool | None = None
    attr_no_edit: bool | None = None
    autoneg: bool | None = None
    bytes_r: int | None = json_field("bytes-r", default=None)
    dns: list[str] | None = None
    dot1x_mode: str | None = None
    dot1x_status: str | None = None
    enable: bool | None = None
    flowctrl_rx: bool | None = None
    flowctrl_tx: bool | None = None
    full_duplex: bool | None = None
    gateway: str | None = None
    ip: str | None = None
    is_uplink: bool | None = None
    jumbo: bool | None = None
    lldp_table: list[DevicePortTableLldpTable] = field(default_factory=list)
    mac: str | None = None
    mac_table: list[DevicePortTableMacTable] = field(default_factory=list)
    masked: bool | None = None
    media: str | None = None
    port_name: str | None = json_field("name", default=None)
    netmask: str | None = None
    op_mode: str | None = None
    poe_caps: int | None = None
    poe_class: str | None = None
    poe_current: str | None = None
    poe_enable: bool | None = None
    poe_good: bool | None = None
    poe_mode: str | None = None
    poe_power: str | None = None
    poe_voltage: str | None = None
    port_delta: DevicePortTablePortDelta | None = None
    port_poe: bool | None = None
    portconf_id: str | None = None
    rx_broadcast: int | None = None
    rx_bytes: int | None = None
    rx_bytes_r: int = json_field("rx_bytes-r", default=None)  # type: ignore
    rx_dropped: int | None = None
    rx_errors: int | None = None
    rx_multicast: int | None = None
    rx_packets: int | None = None
    satisfaction: int | None = None
    satisfaction_reason: int | None = None
    speed: int | None = None
    speed_caps: int | None = None
    stp_pathcost: int | None = None
    stp_state: str | None = None
    tx_broadcast: int | None = None
    tx_bytes: int | None = None
    tx_bytes_r: int = json_field("tx_bytes-r", default=None)  # type: ignore
    tx_dropped: int | None = None
    tx_errors: int | None = None
    tx_multicast: int | None = None
    tx_packets: int | None = None

    ifname: str | None = None
    port_idx: int = 0
    up: bool = False

    @property
    def name(self) -> str:
        """Port name."""
        if not self.port_name:
            # Unifi controller allows to set an empty port name, but it
            # shows up as "Port N" consistently across UI. We mirror the
            # behavior, as empty name is rarely visually helpful.
            return f"Port {self.port_idx}"
        return self.port_name

    def __repr__(self) -> str:
        """Return the representation."""
        return f"<{self.name}: Poe {self.poe_enable}>"


@dataclass
class DeviceRadioTable(ApiItem):
    """Device radio table type definition."""

    antenna_gain: int = 0
    builtin_ant_gain: int = 0
    builtin_antenna: bool = False
    channel: int = 0
    current_antenna_gain: int = 0
    hard_noise_floor_enabled: bool = False
    has_dfs: bool = False
    has_fccdfs: bool = False
    ht: str = ""
    is_11ac: bool = False
    max_txpower: int = 0
    min_rssi_enabled: bool = False
    min_txpower: int = 0
    name: str = ""
    nss: int = 0
    radio: str = ""
    radio_caps: int = 0
    sens_level_enabled: bool = False
    tx_power_mode: str = ""
    wlangroup_id: str = ""


@dataclass
class DeviceRadioTableStats(ApiItem):
    """Device radio table statistics type definition."""

    ast_be_xmit: int = 0
    ast_cst: int = 0
    ast_txto: int = 0
    channel: int = 0
    cu_self_rx: int = 0
    cu_self_tx: int = 0
    cu_total: int = 0
    extchannel: int = 0
    gain: int = 0
    guest_num_sta: int = json_field("guest_num-sta", default=0)  # type: ignore
    name: str = ""
    num_sta: int = 0
    radio: str = ""
    satisfaction: int = 0
    state: str = ""
    tx_packets: str = ""
    tx_power: str = ""
    tx_retries: str = ""
    user_num_sta: str = ""


@dataclass
class DeviceSwitchCaps(ApiItem):
    """Device switch caps type definition."""

    feature_caps: int = 0
    max_aggregate_sessions: int = 0
    max_mirror_sessions: int = 0
    vlan_caps: int = 0


@dataclass
class DeviceSysStats(ApiItem):
    """Device sys stats type definition."""

    loadavg_1: str = ""
    loadavg_15: str = ""
    loadavg_5: str = ""
    mem_buffer: int = 0
    mem_total: int = 0
    mem_used: int = 0


@dataclass
class DeviceSystemStats(ApiItem):
    """Device system stats type definition."""

    cpu: str = ""
    mem: str = ""
    uptime: str = ""


@dataclass
class DeviceTemperature(ApiItem):
    """Device temperature type definition."""

    name: str = ""
    type: str = ""
    value: float = 0.0


@dataclass
class DeviceUplink(ApiItem):
    """Device uplink type definition."""

    full_duplex: bool = False
    ip: str = ""
    mac: str = ""
    max_speed: int = 0
    max_vlan: int = 0
    media: str = ""
    name: str = ""
    netmask: str = ""
    num_port: int = 0
    rx_bytes: int = 0
    rx_bytes_r: int = 0
    rx_dropped: int = 0
    rx_errors: int = 0
    rx_multicast: int = 0
    rx_packets: int = 0
    speed: int = 0
    tx_bytes: int = 0
    tx_bytes_r: int = 0
    tx_dropped: int = 0
    tx_errors: int = 0
    tx_packets: int = 0
    type: str = ""
    up: bool = False
    uplink_mac: str = ""
    uplink_remote_port: int = 0


@dataclass
class DeviceUptimeStatsWanMonitor(ApiItem):
    """Device uptime stats wan monitor type definition."""

    availability: float = 0.0
    target: str = ""
    type: str = ""

    latency_average: int | None = None


@dataclass
class DeviceUptimeStatsWan(ApiItem):
    """Device uptime stats wan type definition."""

    monitors: list[DeviceUptimeStatsWanMonitor]


@dataclass
class DeviceUptimeStats(ApiItem):
    """Device uptime stats type definition."""

    WAN: DeviceUptimeStatsWan
    WAN2: DeviceUptimeStatsWan


@dataclass
class DeviceWlanOverrides(ApiItem):
    """Device wlan overrides type definition."""

    name: str = ""
    radio: str = ""
    radio_name: str = ""
    wlan_id: str = ""


@dataclass
class DeviceSpeedtestStatus(ApiItem):
    """Device speedtest status type definition."""

    latency: int = 0
    rundate: int = 0
    runtime: int = 0
    status_download: int = 0
    status_ping: int = 0
    status_summary: int = 0
    status_upload: int = 0
    xput_download: float = 0.0
    xput_upload: float = 0.0


@dataclass
class DeviceStorage(ApiItem):
    """Device storage type definition."""

    mount_point: str = ""
    name: str = ""
    size: int = 0
    type: str = ""
    used: int = 0


@dataclass
class Device(ApiItem):
    """Device type definition."""

    _id: str = ""
    _uptime: int = 0
    adoptable_when_upgraded: bool = False
    adopted: bool = False
    antenna_table: list[DeviceAntennaTable] = field(default_factory=list)
    architecture: str = ""
    adoption_completed: int = 0
    bytes: int = 0
    bytes_d: int = 0
    bytes_r: int = 0
    cfgversion: int = 0
    config_network: DeviceConfigNetwork | None = None
    connect_request_ip: str = ""
    connect_request_port: str = ""
    considered_lost_at: int = 0
    country_code: int = 0
    countrycode_table: list = field(default_factory=list)
    device_id: str = ""
    dhcp_server_table: list = field(default_factory=list)
    disconnection_reason: str = ""
    displayable_version: str = ""
    dot1x_portctrl_enabled: bool = False
    downlink_table: list = field(default_factory=list)
    element_ap_serial: str = ""
    element_peer_mac: str = ""
    element_uplink_ap_mac: str = ""
    ethernet_overrides: list[DeviceEthernetOverrides] = field(default_factory=list)
    ethernet_table: list[DeviceEthernetTable] = field(default_factory=list)
    fan_level: int | None = None
    flowctrl_enabled: bool = False
    fw_caps: int = 0
    gateway_mac: str = ""
    guest_num_sta: int = 0
    guest_wlan_num_sta: int = 0
    guest_token: str = ""
    has_eth1: bool = False
    has_fan: bool = False
    has_speaker: bool = False
    has_temperature: bool = False
    hash_id: str = ""
    hide_ch_width: str = ""
    hw_caps: int = 0
    inform_ip: str = ""
    inform_url: str = ""
    internet: bool = False
    isolated: bool = False
    jumboframe_enabled: bool = False
    kernel_version: str = ""
    known_cfgversion: str = ""
    last_seen: int = 0
    last_uplink: DeviceLastUplink | None = None
    lcm_brightness: int = 0
    lcm_brightness_override: bool = False
    lcm_idle_timeout_override: bool = False
    lcm_night_mode_begins: str = ""
    lcm_night_mode_enabled: bool = False
    lcm_night_mode_ends: str = ""
    lcm_tracker_enabled: bool = False
    led_override: str = ""
    led_override_color: str = ""
    led_override_color_brightness: int = 0
    license_state: str = ""
    lldp_table: list[DeviceLldpTable] = field(default_factory=list)
    locating: bool = False
    mac: str = ""
    manufacturer_id: int = 0
    meshv3_peer_mac: str = ""
    model: str = ""
    model_in_eol: bool = False
    model_in_lts: bool = False
    model_incompatible: bool = False
    name: str = ""
    network_table: list[DeviceNetworkTable] = field(default_factory=list)
    next_heartbeat_at: int = 0
    next_interval: int = 30
    num_desktop: int = 0
    num_handheld: int = 0
    num_mobile: int = 0
    num_sta: int = 0
    outdoor_mode_override: str = ""
    outlet_ac_power_budget: str = ""
    outlet_ac_power_consumption: str = ""
    outlet_enabled: bool = False
    outlet_overrides: list[DeviceOutletOverrides] = field(default_factory=list)
    outlet_table: list[Outlet] = field(default_factory=list)
    overheating: bool = False
    power_source_ctrl_enabled: bool = False
    prev_non_busy_state: int = 0
    provisioned_at: int = 0
    port_overrides: list[DevicePortOverrides] = field(default_factory=list)
    radio_table: list[DeviceRadioTable] = field(default_factory=list)
    radio_table_stats: list[DeviceRadioTableStats] = field(default_factory=list)
    required_version: str = ""
    rollupgrade: bool = False
    rx_bytes: int = 0
    rx_bytes_d: int = 0
    satisfaction: int = 0
    scan_radio_table: list = field(default_factory=list)
    scanning: bool = False
    serial: str = ""
    site_id: str = ""
    spectrum_scanning: bool = False
    speedtest_status: DeviceSpeedtestStatus | None = json_field(
        "speedtest-status", default=None
    )
    ssh_session_table: list = field(default_factory=list)
    start_connected_millis: int = 0
    start_disconnected_millis: int = 0
    stat: dict | None = None
    state: int = 0
    storage: list[DeviceStorage] | None = None
    stp_priority: str = ""
    stp_version: str = ""
    switch_caps: DeviceSwitchCaps | None = None
    sys_error_caps: int = 0
    sys_stats: DeviceSysStats | None = None
    syslog_key: str = ""
    system_stats: DeviceSystemStats | None = json_field("system-stats", default=None)
    temperatures: list[DeviceTemperature] | None = None
    two_phase_adopt: bool = False
    tx_bytes: int = 0
    tx_bytes_d: int = 0
    type: str = ""
    unsupported: bool = False
    unsupported_reason: int = 0
    upgradable: bool = False
    upgrade_state: int = 0
    upgrade_to_firmware: str = ""
    uplink: DeviceUplink | None = None
    uplink_depth: int | None = None
    uplink_table: list = field(default_factory=list)
    uptime: int = 0
    uptime_stats: DeviceUptimeStats | None = None
    user_num_sta: int | None = json_field("user-num_sta", default=None)  # type: ignore
    user_wlan_num_sta: int = 0
    usg_caps: int = 0
    vap_table: list[dict] = field(default_factory=list)
    version: str = ""
    vwire_enabled: bool = json_field("vwireEnabled", default=False)
    vwire_table: list = field(default_factory=list)
    vwire_vap_table: list = field(default_factory=list)
    wifi_caps: int = 0
    wlan_overrides: list[DeviceWlanOverrides] = field(default_factory=list)
    wlangroup_id_na: str = ""
    wlangroup_id_ng: str = ""
    x_aes_gcm: bool = False
    x_authkey: str = ""
    x_fingerprint: str = ""
    x_has_ssh_hostkey: bool = False
    x_inform_authkey: str = ""
    x_ssh_hostkey_fingerprint: str = ""
    x_vwirekey: str = ""

    disabled: bool = False
    board_revision: int = json_field("board_rev", default=None)  # type: ignore
    general_temperature: int | None = None
    ip: str = ""
    port_table: list[Port] = field(default_factory=list)

    @property
    def id(self) -> str:
        """ID of device."""
        return self.device_id

    @property
    def supports_led_ring(self) -> bool:
        """Check if the hardware supports an LED ring based on the second bit of `hw_caps`."""
        return bool(self.hw_caps & HardwareCapability.LED_RING)

    def __repr__(self) -> str:
        """Return the representation."""
        return f"<Device {self.name}: {self.mac}>"


class DeviceState(enum.IntEnum):
    """Enum for device states."""

    DISCONNECTED = 0
    CONNECTED = 1
    PENDING = 2
    FIRMWARE_MISMATCH = 3
    UPGRADING = 4
    PROVISIONING = 5
    HEARTBEAT_MISSED = 6
    ADOPTING = 7
    DELETING = 8
    INFORM_ERROR = 9
    ADOPTION_FALIED = 10
    ISOLATED = 11

    UNKNOWN = -1

    @classmethod
    def _missing_(cls, value: object) -> DeviceState:
        """Set default enum member if an unknown value is provided."""
        LOGGER.warning("Unsupported device state %s %s", value, cls)
        return DeviceState.UNKNOWN


class HardwareCapability(enum.IntFlag):
    """Enumeration representing hardware capabilities."""

    LED_RING = 2


@dataclass
class DeviceListRequest(ApiRequest):
    """Request object for device list."""

    def __init__(self):
        """Create device list request."""
        super().__init__(method="get", path="/stat/device")


@dataclass
class DevicePowerCyclePortRequest(ApiRequest):
    """Request object for power cycle PoE port."""

    def __init__(self, mac: str, port_idx: int):
        """Create power cycle of PoE request."""
        super().__init__(
            method="post",
            path="/cmd/devmgr",
            data={
                "cmd": "power-cycle",
                "mac": mac,
                "port_idx": port_idx,
            },
        )


@dataclass
class DeviceRestartRequest(ApiRequest):
    """Request object for device restart."""

    def __init__(self, mac: str, soft: bool = True):
        """Create device restart request.

        Hard is specifically for PoE switches and will additionally cycle PoE ports.
        """
        super().__init__(
            method="post",
            path="/cmd/devmgr",
            data={
                "cmd": "restart",
                "mac": mac,
                "reboot_type": "soft" if soft else "hard",
            },
        )


@dataclass
class DeviceUpgradeRequest(ApiRequest):
    """Request object for device upgrade."""

    def __init__(self, mac: str):
        """Create device upgrade request."""
        super().__init__(
            method="post",
            path="/cmd/devmgr",
            data={
                "cmd": "upgrade",
                "mac": mac,
            },
        )


@dataclass
class DeviceSetOutletRelayRequest(ApiRequest):
    """Request object for outlet relay state."""

    def __init__(self, device: Device, outlet_idx: int, state: bool):
        """Create device outlet relay state request.

        True:  outlet power output on.
        False: outlet power output off.
        """
        existing_override = False
        for outlet_override in device.outlet_overrides:
            if outlet_idx == outlet_override.index:
                outlet_override.relay_state = state
                existing_override = True
                break

        if not existing_override:
            name = device.outlet_table[outlet_idx - 1].name
            device.outlet_overrides.append(
                DeviceOutletOverrides(index=outlet_idx, name=name, relay_state=state)
            )

        outlet_overrides = [
            outlet_override.to_json() for outlet_override in device.outlet_overrides
        ]
        super().__init__(
            method="put",
            path=f"/rest/device/{device.id}",
            data={"outlet_overrides": outlet_overrides},
        )


@dataclass
class DeviceSetOutletCycleEnabledRequest(ApiRequest):
    """Request object for outlet cycle_enabled flag."""

    def __init__(self, device: Device, outlet_idx: int, state: bool):
        """Create device outlet outlet cycle_enabled flag request.

        True:  UniFi Network will power cycle this outlet if the internet goes down.
        False: UniFi Network will not power cycle this outlet if the internet goes down.
        """
        existing_override = False
        for outlet_override in device.outlet_overrides:
            if outlet_idx == outlet_override.index:
                outlet_override.cycle_enabled = state
                existing_override = True
                break

        if not existing_override:
            name = device.outlet_table[outlet_idx - 1].name
            device.outlet_overrides.append(
                DeviceOutletOverrides(index=outlet_idx, name=name, cycle_enabled=state)
            )
        super().__init__(
            method="put",
            path=f"/rest/device/{device.id}",
            data={
                "outlet_overrides": [
                    override.to_json() for override in device.outlet_overrides
                ]
            },
        )


@dataclass
class DeviceSetPoePortModeRequest(ApiRequest):
    """Request object for setting port PoE mode."""

    def __init__(
        self,
        device: Device,
        port_idx: int | None = None,
        mode: str | None = None,
        targets: list[tuple[int, str]] | None = None,
    ):
        """Create device set port PoE mode request.

        Auto, 24v, passthrough, off.
        Make sure to not overwrite any existing configs.
        """
        overrides: list[tuple[int, str]] = []
        if port_idx is not None and mode is not None:
            overrides.append((port_idx, mode))
        elif targets is not None:
            overrides = targets
        else:
            raise AttributeError

        port_overrides = deepcopy(device.port_overrides)

        for override in overrides:
            port_idx, mode = override

            existing_override = False
            for port_override in port_overrides:
                if port_idx == port_override.port_idx:
                    port_override.poe_mode = mode
                    existing_override = True
                    break

            if existing_override:
                continue

            port_override = DevicePortOverrides(port_idx=port_idx, poe_mode=mode)
            if portconf_id := device.port_table[port_idx - 1].portconf_id:
                port_override.portconf_id = portconf_id
            port_overrides.append(port_override)
        super().__init__(
            method="put",
            path=f"/rest/device/{device.id}",
            data={
                "port_overrides": [override.to_json() for override in port_overrides]
            },
        )


@dataclass
class DeviceSetLedStatus(ApiRequest):
    """Request object for setting LED status of device."""

    def __init__(
        self,
        device: Device,
        status: str = "on",
        brightness: int | None = None,
        color: str | None = None,
    ):
        """Set LED status of device."""

        data: dict[str, int | str] = {"led_override": status}
        if device.supports_led_ring:
            # Validate brightness parameter
            if brightness is not None:
                if not (0 <= brightness <= 100):
                    raise AttributeError(
                        "Brightness must be within the range [0, 100]."
                    )
                data["led_override_color_brightness"] = brightness

            # Validate color parameter
            if color is not None:
                if not re.match(r"^#(?:[0-9a-fA-F]{3}){1,2}$", color):
                    raise AttributeError(
                        "Color must be a valid hex color code (e.g., '#00FF00')."
                    )
                data["led_override_color"] = color

        super().__init__(
            method="put",
            path=f"/rest/device/{device.id}",
            data=data,
        )
