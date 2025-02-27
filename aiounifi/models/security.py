"""Security models related to firewall groups and rules."""

from dataclasses import dataclass, field

from .api import ApiItem, ApiRequest


@dataclass
class FirewallGroupRequest(ApiRequest):
    """Request object for device list."""

    def __init__(self):
        """Create device list request."""
        super().__init__(method="get", path="/rest/firewallgroup")


@dataclass
class FirewallGroup(ApiItem):
    """Firewall group type definition."""

    _id: str | None = None
    group_members: list[str] = field(default_factory=list)
    group_type: str | None = None
    name: str | None = None
    site_id: str | None = None


class FirewallAddressGroup(FirewallGroup):
    """Represents a firewall address group."""


class FirewallPortGroup(FirewallGroup):
    """Represents a firewall port group."""


@dataclass
class FirewallRule(ApiItem):
    """Firewall rule type definition."""

    _id: str | None = None
    action: str | None = None
    dst_address: str | None = None
    dst_firewallgroup_ids: list[str] = field(default_factory=list)
    dst_networkconf_id: str | None = None
    dst_networkconf_type: str | None = None
    dst_port: str | None = None
    enabled: bool | None = None
    icmp_typename: str | None = None
    ipsec: str | None = None
    logging: bool | None = None
    name: str | None = None
    protocol: str | None = None
    protocol_match_excepted: bool | None = None
    rule_index: int | None = None
    ruleset: str | None = None
    setting_preference: str | None = None
    site_id: str | None = None
    src_firewallgroup_ids: list[str] = field(default_factory=list)
    src_networkconf_id: str | None = None
    src_networkconf_type: str | None = None
    state_new: bool | None = None
    state_established: bool | None = None
    src_address: str | None = None
    src_mac_address: str | None = None
    state_invalid: bool | None = None
    state_related: bool | None = None
    src_port: str | None = None


@dataclass
class FirewallRuleRequest(ApiRequest):
    """Request object for firewall rules list."""

    def __init__(self):
        """Create firewall rule request."""
        super().__init__(method="get", path="/rest/firewallrule")


@dataclass
class FirewallAddressGroupRequest(ApiRequest):
    """Request object for firewall address groups list."""

    def __init__(self):
        """Create device list request."""
        super().__init__(
            method="get", path="/rest/firewallgroup?group_type=address-group"
        )


@dataclass
class FirewallPortGroupRequest(ApiRequest):
    """Request object for firewall port groups list."""

    def __init__(self):
        """Create device list request."""
        super().__init__(method="get", path="/rest/firewallgroup?group_type=port-group")
