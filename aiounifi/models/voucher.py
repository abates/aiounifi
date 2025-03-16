"""Hotspot vouchers as part of a UniFi network."""

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import StrEnum

from .api import ApiItem, json_field


class VoucherStatus(StrEnum):
    """Voucher status."""

    VALID_ONE = "VALID_ONE"
    VALID_MULTI = "VALID_MULTI"
    USED_MULTIPLE = "USED_MULTIPLE"


def convert_to_seconds(seconds: float):
    """Convert a float to seconds in a timedelta."""
    return timedelta(seconds=seconds)


@dataclass
class VoucherCode:
    """A string that represents a voucher code."""

    code: str

    def __str__(self):
        """Get the human readable string representation."""
        return f"{self.code[:5]}-{self.code[5:]}"


@dataclass
class Voucher(ApiItem):
    """Voucher type definition."""

    duration: timedelta = json_field(custom_initializer=convert_to_seconds)
    id: str = json_field("_id")

    admin_name: str | None = None
    for_hotspot: bool | None = None
    note: str = ""
    qos_overwrite: bool | None = None
    qos_usage_quota: int = 0
    qos_rate_max_up: int = 0
    qos_rate_max_down: int = 0
    quota: int | None = None
    site_id: str | None = None
    status: VoucherStatus | None = None
    used: int | None = None
    code: VoucherCode | None = None

    create_time: datetime = json_field(
        custom_initializer=datetime.fromtimestamp, default=None
    )
    end_time: float | None = json_field(
        custom_initializer=datetime.fromtimestamp, default=None
    )
    start_time: float | None = json_field(
        custom_initializer=datetime.fromtimestamp, default=None
    )
    status_expires: float = json_field(
        custom_initializer=convert_to_seconds, default=None
    )
