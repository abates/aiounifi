"""Clients are devices on a UniFi network."""

from dataclasses import dataclass

from .api import ApiItem, json_field


@dataclass
class Client(ApiItem):
    """Represents a client network device."""

    _id: str | None = None
    _is_guest_by_uap: bool | None = None
    is_guest_by_switch: bool = json_field("_is_guest_by_usw", default=False)
    is_guest_by_gateway: bool = json_field("_is_guest_by_ugw", default=False)
    anomalies: int | None = None
    access_point_mac: str = json_field("ap_mac", default="")
    association_time: int = json_field("assoc_time", default=0)
    authorized: bool | None = None
    blocked: bool = False
    bssid: str | None = None
    bytes_r: int = json_field("bytes-r", default=0)
    ccq: int | None = None
    channel: int | None = None
    dev_cat: int | None = None
    dev_family: int | None = None
    dev_id: int | None = None
    dev_id_override: int | None = None
    dev_vendor: int | None = None
    device_name: str = ""
    dhcpend_time: int | None = None
    disconnect_timestamp: int | None = None
    eagerly_discovered: bool | None = None
    essid: str = ""
    fingerprint_engine_version: str | None = None
    fingerprint_override: bool | None = None
    fingerprint_source: int | None = None
    first_seen: int = 0
    fixed_ip: str = ""
    firmware_version: str = json_field("fw_version", default="")
    gw_mac: str | None = None
    hostname: str = ""
    hostname_source: str | None = None
    idle_time: int = json_field("idletime", default=0)
    ip: str = ""
    is_11r: bool | None = None
    is_guest: bool = False
    is_wired: bool = False
    last_seen: int = 0
    last_seen_by_access_point: int = json_field("_last_seen_by_uap", default=0)
    last_seen_by_gateway: int = json_field("_last_seen_by_ugw", default=0)
    last_seen_by_switch: int = json_field("_last_seen_by_usw", default=0)
    latest_association_time: int = json_field("latest_assoc_time", default=0)
    mac: str = ""
    name: str = ""
    network: str | None = None
    network_id: str | None = None
    noise: int | None = None
    noted: bool | None = None
    os_class: int | None = None
    os_name: int | None = None
    oui: str = ""
    powersave_enabled: bool | None = None
    qos_policy_applied: bool | None = None
    radio: str | None = None
    radio_name: str | None = None
    radio_proto: str | None = None
    rssi: int | None = None
    rx_bytes: int = 0
    rx_bytes_r: float = json_field("rx_bytes-r", default=0.0)
    rx_packets: int | None = None
    rx_rate: int | None = None
    satisfaction: int | None = None
    score: int | None = None
    signal: int | None = None
    site_id: str = ""
    switch_depth: int = json_field("sw_depth", default=None)
    switch_mac: str = json_field("sw_mac", default="")
    switch_port: int = json_field("sw_port", default=None)
    tx_bytes: int = 0
    tx_bytes_r: float = json_field("tx_bytes-r", default=0.0)
    tx_packets: int | None = None
    tx_power: int | None = None
    tx_rate: int | None = None
    tx_retries: int | None = None
    uptime: int = 0
    uptime_by_access_point: int = json_field("_uptime_by_uap", default=0)
    uptime_by_gateway: int = json_field("_uptime_by_ugw", default=0)
    uptime_by_switch: int = json_field("_uptime_by_usw", default=0)
    use_fixedip: bool | None = None
    user_id: str | None = None
    usergroup_id: str | None = None
    vlan: int | None = None
    wifi_tx_attempts: int | None = None
    wired_rate_mbps: int = 0
    wired_tx_bytes: int = json_field("wired-tx_bytes", default=0)
    wired_rx_bytes: int = json_field("wired-rx_bytes", default=0)
    wired_tx_packets: int = json_field("wired-tx_packets", default=0)
    wired_rx_packets: int = json_field("wired-rx_packets", default=0)
    wired_tx_bytes_r: float = json_field("wired-tx_bytes-r", default=0.0)
    wired_rx_bytes_r: float = json_field("wired-rx_bytes-r", default=0.0)
