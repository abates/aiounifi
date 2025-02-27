"""The security endpoint manages many things including firewall groups and rules."""

from ..models.message import MessageKey
from ..models.security import (
    FirewallAddressGroup,
    FirewallAddressGroupRequest,
    FirewallPortGroup,
    FirewallPortGroupRequest,
    FirewallRule,
    FirewallRuleRequest,
)
from .api_handlers import APIHandler


class FirewallAddressGroups(APIHandler[FirewallAddressGroup]):
    """Represents firewall address groups."""

    obj_id_key = "_id"
    item_cls = FirewallAddressGroup
    process_messages = (MessageKey.FIREWALL_ADDRESS_GROUP_UPDATED,)
    api_request = FirewallAddressGroupRequest()


class FirewallPortGroups(APIHandler[FirewallPortGroup]):
    """Represents firewall port groups."""

    obj_id_key = "_id"
    item_cls = FirewallPortGroup
    process_messages = (MessageKey.FIREWALL_PORT_GROUP_UPDATED,)
    api_request = FirewallPortGroupRequest()


class FirewallRules(APIHandler[FirewallRule]):
    """Represents firewall port groups."""

    obj_id_key = "_id"
    item_cls = FirewallRule
    process_messages = (MessageKey.FIREWALL_RULE_UPDATED,)
    api_request = FirewallRuleRequest()
