"""Test client configuration API.

pytest --cov-report term-missing --cov=aiounifi.clients tests/test_clients.py
"""

from typing import Any

import pytest

from aiounifi.controller import Controller


@pytest.mark.parametrize(
    "network_conf_payload",
    [
        [
            {
                "setting_preference": "manual",
                "dhcpdv6_dns_auto": True,
                "ipv6_pd_stop": "::7d1",
                "dhcpd_gateway_enabled": True,
                "dhcpd_dns_1": "1.1.1.1",
                "ipv6_client_address_assignment": "slaac",
                "dhcpd_start": "192.168.0.100",
                "dhcpd_unifi_controller": "",
                "ipv6_ra_enabled": True,
                "domain_name": "localdomain",
                "ip_subnet": "192.168.0.0/24",
                "ipv6_interface_type": "none",
                "dhcpdv6_stop": "::7d1",
                "is_nat": True,
                "dhcpdv6_enabled": False,
                "dhcpd_dns_enabled": True,
                "dhcp_relay_enabled": True,
                "dhcpd_conflict_checking": True,
                "name": "Management Network",
                "site_id": "5e231c10931eb902acf25112",
                "dhcpdv6_leasetime": 86400,
                "ipv6_enabled": True,
                "_id": "012345678910111213141516",
                "lte_lan_enabled": True,
                "purpose": "corporate",
                "dhcpd_leasetime": 86400,
                "igmp_snooping": False,
                "dhcpd_time_offset_enabled": False,
                "dhcpguard_enabled": False,
                "ipv6_ra_preferred_lifetime": 14400,
                "dhcpd_stop": "192.168.0.254",
                "enabled": True,
                "dhcpd_enabled": False,
                "dhcpd_wpad_url": "",
                "networkgroup": "LAN",
                "dhcpdv6_start": "::2",
                "vlan_enabled": False,
                "ipv6_setting_preference": "auto",
                "dhcpd_gateway": "192.168.0.1",
                "gateway_type": "default",
                "ipv6_ra_priority": "high",
                "dhcpd_boot_enabled": False,
                "ipv6_pd_start": "::2",
                "upnp_lan_enabled": False,
                "dhcpd_ntp_enabled": False,
                "mdns_enabled": False,
                "attr_no_delete": True,
                "attr_hidden_id": "LAN",
                "dhcpd_tftp_server": "",
                "auto_scale_enabled": False,
            },
            {
                "setting_preference": "manual",
                "purpose": "wan",
                "wan_type_v6": "disabled",
                "wan_dhcpv6_pd_size_enabled": False,
                "wan_vlan": "",
                "wan_dhcp_options": [],
                "ipv6_wan_delegation_type": "none",
                "igmp_proxy_upstream": False,
                "wan_load_balance_type": "failover-only",
                "mac_override_enabled": False,
                "ipv6_setting_preference": "manual",
                "wan_ipv6_dns_preference": "auto",
                "wan_dns2": "",
                "wan_dns1": "172.16.2.100",
                "wan_ipv6_dns1": "",
                "wan_ipv6_dns2": "",
                "wan_networkgroup": "WAN",
                "wan_provider_capabilities": {
                    "upload_kilobits_per_second": 100000,
                    "download_kilobits_per_second": 100000,
                },
                "wan_ip_aliases": [],
                "wan_smartq_enabled": False,
                "wan_dns_preference": "manual",
                "wan_load_balance_weight": 50,
                "wan_vlan_enabled": False,
                "site_id": "5e231c10931eb902acf25112",
                "name": "WAN Provider",
                "wan_ip": "192.168.1.1",
                "report_wan_event": False,
                "ipv6_enabled": True,
                "_id": "012345678910111213141517",
                "attr_no_delete": True,
                "wan_type": "dhcp",
                "attr_hidden_id": "WAN",
            },
            {
                "setting_preference": "manual",
                "dhcpdv6_dns_auto": True,
                "ipv6_pd_stop": "::7d1",
                "dhcpd_gateway_enabled": False,
                "ipv6_client_address_assignment": "slaac",
                "dhcpd_unifi_controller": "",
                "dhcpd_start": "192.168.1.100",
                "ipv6_ra_enabled": True,
                "domain_name": "",
                "ip_subnet": "192.168.1.0/24",
                "ipv6_interface_type": "none",
                "dhcpdv6_stop": "::7d1",
                "is_nat": True,
                "dhcpd_dns_enabled": False,
                "dhcpdv6_enabled": False,
                "dhcp_relay_enabled": True,
                "dhcpd_conflict_checking": True,
                "dhcpd_wins_enabled": False,
                "name": "VLAN 2",
                "site_id": "5e231c10931eb902acf25112",
                "dhcpdv6_leasetime": 86400,
                "ipv6_enabled": True,
                "_id": "012345678910111213141518",
                "lte_lan_enabled": False,
                "purpose": "corporate",
                "dhcpd_leasetime": 86400,
                "igmp_snooping": True,
                "dhcpd_time_offset_enabled": False,
                "dhcpguard_enabled": False,
                "ipv6_ra_preferred_lifetime": 14400,
                "enabled": True,
                "dhcpd_stop": "192.168.1.254",
                "dhcpd_enabled": False,
                "vlan": "2",
                "dhcpd_wpad_url": "",
                "networkgroup": "LAN",
                "ipv6_ra_valid_lifetime": "86400",
                "dhcpdv6_start": "::2",
                "vlan_enabled": True,
                "ipv6_setting_preference": "auto",
                "gateway_type": "default",
                "ipv6_ra_priority": "high",
                "dhcpd_boot_enabled": False,
                "ipv6_pd_start": "::2",
                "upnp_lan_enabled": False,
                "dhcpd_ntp_enabled": False,
                "mdns_enabled": False,
                "dhcpdv6_dns_1": "",
                "dhcpd_tftp_server": "",
                "auto_scale_enabled": False,
            },
        ],
    ],
)
@pytest.mark.usefixtures("_mock_endpoints")
async def test_networks(
    unifi_controller: Controller, network_conf_payload: list[dict[str, Any]]
) -> None:
    """Test sites class."""
    networks = unifi_controller.networks
    await networks.update()
    assert len(networks.items()) == len(network_conf_payload)

    def check(want_items, got_item):
        for key, want in want_items.items():
            got = got_item[key]
            if isinstance(want, dict):
                check(want, got)
            else:
                assert want == got

    for i, network in enumerate(networks.values()):
        check(network_conf_payload[i], network.raw)
