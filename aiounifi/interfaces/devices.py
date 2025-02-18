"""UniFi devices are network infrastructure.

Access points, gateways, power plugs, switches.
"""

from ..models.api import ApiResponse
from ..models.device import Device, DeviceListRequest, DeviceUpgradeRequest
from ..models.message import MessageKey
from .api_handlers import APIHandler


class Devices(APIHandler[Device]):
    """Represents network devices."""

    obj_id_key = "mac"
    item_cls = Device
    process_messages = (MessageKey.DEVICE,)
    api_request = DeviceListRequest.create()

    async def upgrade(self, mac: str) -> ApiResponse:
        """Upgrade network device."""
        return await self.controller.request(DeviceUpgradeRequest.create(mac))
