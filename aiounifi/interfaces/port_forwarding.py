"""UniFi port forwarding."""

from aiounifi.models.api import ApiEndpoint

from ..models.message import MessageKey
from ..models.port_forward import PortForward
from .api_handlers import APIHandler


class PortForwarding(APIHandler[PortForward]):
    """Represents port forwarding."""

    obj_id_key = "_id"
    item_cls = PortForward
    process_messages = (MessageKey.PORT_FORWARD_ADDED, MessageKey.PORT_FORWARD_UPDATED)
    remove_messages = (MessageKey.PORT_FORWARD_DELETED,)
    list_endpoint = ApiEndpoint(path="/rest/portforward")
    update_endpoint = ApiEndpoint(path="/rest/portforward/{api_item.id}")

    async def disable(self, port_forward: PortForward):
        """Disable a port forward."""
        return await self.set_enabled(port_forward, False)

    async def enable(self, port_forward: PortForward):
        """Enable a port forward."""
        return await self.set_enabled(port_forward, True)

    async def set_enabled(self, port_forward: PortForward, enabled: bool):
        """Set whether or not a port forward is enabled."""
        port_forward.enabled = enabled
        return await self.save(port_forward, {"enabled"})
