"""Security models related to firewall groups and rules."""

from dataclasses import dataclass
from typing import Self

from .api import ApiItem, ApiRequest


@dataclass
class NetworkConfRequest(ApiRequest):
    """Request object for network configuration list."""

    @classmethod
    def create(cls) -> Self:
        """Create device list request."""
        return cls(method="get", path="/rest/networkconf")


@dataclass
class NetworkConf(ApiItem):
    """Network conf type definition."""

    _id: str | None = None
    attr_hidden_id: str | None = None
    attr_no_delete: bool | None = None
    auto_scale_enabled: bool | None = None
    dhcp_relay_enabled: bool | None = None
    dhcpd_boot_enabled: bool | None = None
    dhcpd_conflict_checking: bool | None = None
    dhcpd_dns_1: str | None = None
    dhcpd_dns_enabled: bool | None = None
    dhcpd_enabled: bool | None = None
    dhcpd_gateway: str | None = None
    dhcpd_gateway_enabled: bool | None = None
    dhcpd_leasetime: int | None = None
    dhcpd_ntp_enabled: bool | None = None
    dhcpd_start: str | None = None
    dhcpd_stop: str | None = None
    dhcpd_tftp_server: str | None = None
    dhcpd_time_offset_enabled: bool | None = None
    dhcpd_unifi_controller: str | None = None
    dhcpd_wpad_url: str | None = None
    dhcpdv6_dns_auto: bool | None = None
    dhcpdv6_enabled: bool | None = None
    dhcpdv6_leasetime: int | None = None
    dhcpdv6_start: str | None = None
    dhcpdv6_stop: str | None = None
    dhcpguard_enabled: bool | None = None
    domain_name: str | None = None
    enabled: bool | None = None
    gateway_type: str | None = None
    igmp_snooping: bool | None = None
    ip_subnet: str | None = None
    ipv6_client_address_assignment: str | None = None
    ipv6_enabled: bool | None = None
    ipv6_interface_type: str | None = None
    ipv6_pd_start: str | None = None
    ipv6_pd_stop: str | None = None
    ipv6_ra_enabled: bool | None = None
    ipv6_ra_preferred_lifetime: int | None = None
    ipv6_ra_priority: str | None = None
    ipv6_setting_preference: str | None = None
    is_nat: bool | None = None
    lte_lan_enabled: bool | None = None
    mdns_enabled: bool | None = None
    name: str | None = None
    networkgroup: str | None = None
    purpose: str | None = None
    setting_preference: str | None = None
    site_id: str | None = None
    upnp_lan_enabled: bool | None = None
    vlan_enabled: str | None = None
