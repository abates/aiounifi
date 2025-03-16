"""The security endpoint manages many things including firewall groups and rules."""

from aiounifi.models.api import ApiEndpoint

from ..models.message import MessageKey
from ..models.security import FirewallAddressGroup, FirewallPortGroup, FirewallRule
from .api_handlers import APIHandler


class FirewallAddressGroups(APIHandler[FirewallAddressGroup]):
    """Represents firewall address groups."""

    obj_id_key = "_id"
    item_cls = FirewallAddressGroup
    process_messages = (MessageKey.FIREWALL_ADDRESS_GROUP_UPDATED,)
    list_endpoint = ApiEndpoint(path="/rest/firewallgroup?group_type=address-group")


class FirewallPortGroups(APIHandler[FirewallPortGroup]):
    """Represents firewall port groups."""

    obj_id_key = "_id"
    item_cls = FirewallPortGroup
    process_messages = (MessageKey.FIREWALL_PORT_GROUP_UPDATED,)
    list_endpoint = ApiEndpoint(path="/rest/firewallgroup?group_type=port-group")


class FirewallRules(APIHandler[FirewallRule]):
    """Represents firewall port groups."""

    obj_id_key = "_id"
    item_cls = FirewallRule
    process_messages = (MessageKey.FIREWALL_RULE_UPDATED,)
    list_endpoint = ApiEndpoint(path="/rest/firewallrule")
