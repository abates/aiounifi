"""WLANs as part of a UniFi network."""

from ..models.api import ApiEndpoint, ApiResponse
from ..models.message import MessageKey
from ..models.wlan import Wlan
from .api_handlers import APIHandler


class Wlans(APIHandler[Wlan]):
    """Represents WLAN configurations."""

    obj_id_key = "_id"
    item_cls = Wlan
    process_messages = (MessageKey.WLAN_CONF_UPDATED,)
    list_endpoint = ApiEndpoint(path="/rest/wlanconf")
    update_endpoint = ApiEndpoint(path="/rest/wlanconf/{api_item.id}")

    async def set_enabled(self, wlan: Wlan, enabled: bool) -> ApiResponse:
        """Block client from controller."""
        wlan.enabled = enabled
        return await self.save(wlan, {"enabled"})

    async def enable(self, wlan: Wlan) -> ApiResponse:
        """Block client from controller."""
        return await self.set_enabled(wlan, True)

    async def disable(self, wlan: Wlan) -> ApiResponse:
        """Unblock client from controller."""
        return await self.set_enabled(wlan, False)
