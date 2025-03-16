"""Security models related to firewall groups and rules."""

from dataclasses import dataclass

from .api import ApiItem


@dataclass
class WanProviderCapabilities(ApiItem):
    download_kilobits_per_second: int | None = None
    upload_kilobits_per_second: int | None = None


@dataclass
class NetworkConf(ApiItem):
    _id: str | None = None
    attr_hidden_id: str | None = None
    attr_no_delete: bool | None = None
    ipv6_enabled: bool | None = None
    ipv6_setting_preference: str | None = None
    name: str | None = None
    purpose: str | None = None
    setting_preference: str | None = None
    site_id: str | None = None


@dataclass
class CorporateNetworkConf(NetworkConf):
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
    dhcpd_wins_enabled: bool | None = None
    dhcpd_wpad_url: str | None = None
    dhcpdv6_allow_slaac: bool | None = None
    dhcpdv6_dns_1: str | None = None
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
    internet_access_enabled: bool | None = None
    ip_subnet: str | None = None
    ipv6_client_address_assignment: str | None = None
    ipv6_interface_type: str | None = None
    ipv6_pd_auto_prefixid_enabled: bool | None = None
    ipv6_pd_start: str | None = None
    ipv6_pd_stop: str | None = None
    ipv6_ra_enabled: bool | None = None
    ipv6_ra_preferred_lifetime: int | None = None
    ipv6_ra_priority: str | None = None
    ipv6_ra_valid_lifetime: str | None = None
    ipv6_subnet: str | None = None
    is_nat: bool | None = None
    lte_lan_enabled: bool | None = None
    mdns_enabled: bool | None = None
    nat_outbound_ip_addresses: list | None = None
    networkgroup: str | None = None
    upnp_lan_enabled: bool | None = None
    vlan: int | None = None
    vlan_enabled: bool | None = None


@dataclass
class WanNetworkConf(NetworkConf):
    igmp_proxy_for: str | None = None
    igmp_proxy_upstream: bool | None = None
    ipv6_wan_delegation_type: str | None = None
    mac_override_enabled: bool | None = None
    report_wan_event: bool | None = None
    single_network_lan: str | None = None
    wan_dhcp_options: list | None = None
    wan_dhcpv6_pd_size: int | None = None
    wan_dhcpv6_pd_size_enabled: bool | None = None
    wan_dns1: str | None = None
    wan_dns2: str | None = None
    wan_dns_preference: str | None = None
    wan_ip: str | None = None
    wan_ip_aliases: list | None = None
    wan_ipv6_dns1: str | None = None
    wan_ipv6_dns2: str | None = None
    wan_ipv6_dns_preference: str | None = None
    wan_load_balance_type: str | None = None
    wan_load_balance_weight: int | None = None
    wan_networkgroup: str | None = None
    wan_provider_capabilities: WanProviderCapabilities | None = None
    wan_smartq_enabled: bool | None = None
    wan_type: str | None = None
    wan_type_v6: str | None = None
    wan_vlan: str | None = None
    wan_vlan_enabled: bool | None = None
