"""Hotspot vouchers as part of a UniFi network."""

from ..models.api import ApiEndpoint, ApiResponse
from ..models.voucher import Voucher
from .api_handlers import APIHandler


class Vouchers(APIHandler[Voucher]):
    """Represents Hotspot vouchers."""

    obj_id_key = "_id"
    item_cls = Voucher
    list_endpoint = ApiEndpoint(path="/stat/voucher")
    create_endpoint = ApiEndpoint(path="/cmd/hotspot")

    async def create(self, voucher: Voucher) -> ApiResponse:
        """Create voucher on controller."""
        data = {
            "cmd": "create-voucher",
            "n": 1,
            "quota": voucher.quota,
            "expire_number": int(voucher.duration.total_seconds() / 60),
            "expire_unit": 1,
        }

        if voucher.qos_usage_quota:
            data["bytes"] = voucher.qos_usage_quota
        if voucher.qos_rate_max_up:
            data["up"] = voucher.qos_rate_max_up
        if voucher.qos_rate_max_down:
            data["down"] = voucher.qos_rate_max_down
        if voucher.note:
            data["note"] = voucher.note

        return await self.client.post(
            self.create_endpoint,
            voucher,
            data=data,
        )

    async def delete(self, voucher: Voucher) -> ApiResponse:
        """Delete voucher from controller."""
        data = {
            "cmd": "delete-voucher",
            "_id": voucher.id,
        }
        return await self.client.post(self.create_endpoint, voucher, data=data)
