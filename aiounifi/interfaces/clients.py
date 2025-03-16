"""Clients are devices on a UniFi network."""

from ..models.api import ApiEndpoint, ApiResponse
from ..models.client import Client
from ..models.message import MessageKey
from .api_handlers import APIHandler


class Clients(APIHandler[Client]):
    """Represents client network devices."""

    obj_id_key = "mac"
    item_cls = Client
    process_messages = (MessageKey.CLIENT,)
    remove_messages = (MessageKey.CLIENT_REMOVED,)
    list_endpoint = ApiEndpoint(path="/stat/sta")

    async def block(self, mac: str) -> ApiResponse:
        """Block client from controller."""
        return await self.send_cmd("block-sta", mac=mac)

    async def reconnect(self, mac: str) -> ApiResponse:
        """Force a wireless client to reconnect to the network."""
        return await self.send_cmd("kick-sta", mac=mac)

    async def remove(self, macs: list[str]) -> ApiResponse:
        """Make controller forget provided clients."""
        return await self.send_cmd("forget-sta", macs=macs)

    async def send_cmd(self, cmd: str, **kwargs) -> ApiResponse:
        """Upgrade network device."""
        return await self.client.post(
            ApiEndpoint(
                path="/cmd/stamgr",
            ),
            None,
            data={"cmd": cmd, **kwargs},
        )

    async def unblock(self, mac: str) -> ApiResponse:
        """Unblock client from controller."""
        return await self.send_cmd("unblock-sta", mac=mac)
