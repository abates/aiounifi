"""Hotspot vouchers as part of a UniFi network."""

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import StrEnum

from .api import ApiItem, ApiRequest, json_field


class VoucherStatus(StrEnum):
    """Voucher status."""

    VALID_ONE = "VALID_ONE"
    VALID_MULTI = "VALID_MULTI"
    USED_MULTIPLE = "USED_MULTIPLE"


@dataclass
class Voucher(ApiItem):
    """Voucher type definition."""

    site_id: str
    quota: int
    used: int
    admin_name: str
    status: VoucherStatus
    voucher_create_time: float = json_field("create_time")
    voucher_duration: float = json_field("duration")
    voucher_status_expires: float = json_field("status_expires")

    id: str = json_field("_id")
    note: str = ""
    qos_overwrite: bool | None = None
    qos_usage_quota: int = 0
    qos_rate_max_up: int = 0
    qos_rate_max_down: int = 0
    for_hotspot: bool | None = None
    voucher_code: str = json_field("code", default="")
    voucher_end_time: float | None = json_field("end_time", default=None)
    voucher_start_time: float | None = json_field("start_time", default=None)

    @property
    def code(self) -> str:
        """Code of voucher in known format 00000-00000.

        To enter the code on the captive portal, the hyphen must be placed after the fifth digit.
        """
        code = self.voucher_code
        # API returns the code without a hyphen. But this is necessary. Separate the API string after the fifth digit.
        return f"{code[:5]}-{code[5:]}"

    @property
    def duration(self) -> timedelta:
        """Expiration of voucher."""
        return timedelta(minutes=self.voucher_duration)

    @property
    def create_time(self) -> datetime:
        """Create datetime of voucher."""
        return datetime.fromtimestamp(self.voucher_create_time)

    @property
    def start_time(self) -> datetime | None:
        """Start datetime of first usage of voucher."""
        if self.voucher_start_time is not None:
            return datetime.fromtimestamp(self.voucher_start_time)
        return None

    @property
    def end_time(self) -> datetime | None:
        """End datetime of latest usage of voucher."""
        if self.voucher_end_time is not None:
            return datetime.fromtimestamp(self.voucher_end_time)
        return None

    @property
    def status_expires(self) -> timedelta | None:
        """Status expires in seconds."""
        if self.voucher_status_expires > 0:
            return timedelta(seconds=self.voucher_status_expires)
        return None


@dataclass
class VoucherListRequest(ApiRequest):
    """Request object for voucher list."""

    def __init__(self):
        """Create voucher list request."""
        super().__init__(
            method="get",
            path="/stat/voucher",
        )


@dataclass
class VoucherCreateRequest(ApiRequest):
    """Request object for voucher create."""

    def __init__(
        self,
        expire_number: int,
        expire_unit: int = 1,
        number: int = 1,
        quota: int = 0,
        usage_quota: int | None = None,
        rate_max_up: int | None = None,
        rate_max_down: int | None = None,
        note: str | None = None,
    ):
        """Create voucher create request.

        :param expire_number: expiration of voucher per expire_unit
        :param expire_unit: scale of expire_number, 1 = minute, 60 = hour, 3600 = day
        :param number: number of vouchers
        :param quota: number of using; 0 = unlimited
        :param usage_quota: quantity of bytes allowed in MB
        :param rate_max_up: up speed allowed in kbps
        :param rate_max_down: down speed allowed in kbps
        :param note: description
        """
        data = {
            "cmd": "create-voucher",
            "n": number,
            "quota": quota,
            "expire_number": expire_number,
            "expire_unit": expire_unit,
        }
        if usage_quota:
            data["bytes"] = usage_quota
        if rate_max_up:
            data["up"] = rate_max_up
        if rate_max_down:
            data["down"] = rate_max_down
        if note:
            data["note"] = note

        super().__init__(
            method="post",
            path="/cmd/hotspot",
            data=data,
        )


@dataclass
class VoucherDeleteRequest(ApiRequest):
    """Request object for voucher delete."""

    def __init__(
        self,
        obj_id: str,
    ):
        """Create voucher delete request."""
        data = {
            "cmd": "delete-voucher",
            "_id": obj_id,
        }
        super().__init__(
            method="post",
            path="/cmd/hotspot",
            data=data,
        )
