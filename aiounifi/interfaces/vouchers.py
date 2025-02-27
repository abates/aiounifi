"""Hotspot vouchers as part of a UniFi network."""

from ..models.api import ApiResponse
from ..models.voucher import (
    Voucher,
    VoucherCreateRequest,
    VoucherDeleteRequest,
    VoucherListRequest,
)
from .api_handlers import APIHandler


class Vouchers(APIHandler[Voucher]):
    """Represents Hotspot vouchers."""

    obj_id_key = "_id"
    item_cls = Voucher
    api_request = VoucherListRequest()

    async def create(self, voucher: Voucher) -> ApiResponse:
        """Create voucher on controller."""
        return await self.controller.request(
            VoucherCreateRequest(
                quota=voucher.quota,
                expire_number=int(
                    voucher.duration.total_seconds() / 60  # Get minutes.
                ),
                usage_quota=voucher.qos_usage_quota,
                rate_max_up=voucher.qos_rate_max_up,
                rate_max_down=voucher.qos_rate_max_down,
                note=voucher.note,
            )
        )

    async def delete(self, voucher: Voucher) -> ApiResponse:
        """Delete voucher from controller."""
        return await self.controller.request(
            VoucherDeleteRequest(
                obj_id=voucher.id,
            )
        )
