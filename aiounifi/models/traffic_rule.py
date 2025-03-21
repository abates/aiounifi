"""Traffic rules as part of a UniFi network."""

from dataclasses import dataclass

from aiounifi.models.traffic import IPAddress, IPRange, TargetDevice

from .api import ApiItem, json_field


@dataclass
class BandwidthLimit(ApiItem):
    """Bandwidth limit type definition."""

    download_limit_kbps: int
    enabled: bool
    upload_limit_kbps: int


@dataclass
class Schedule(ApiItem):
    """Schedule to enable/disable traffic rule type definition."""

    date_end: str
    date_start: str
    mode: str
    repeat_on_days: list[str]
    time_all_day: bool
    time_range_end: str
    time_range_start: str


@dataclass
class TrafficRule(ApiItem):
    """Traffic rule type definition."""

    id: str = json_field("_id")
    action: str | None = None
    app_category_ids: list[str] | None = None
    app_ids: list[str] | None = None
    bandwidth_limit: BandwidthLimit | None = None
    description: str | None = None
    domains: list[str] | None = None
    enabled: bool | None = None
    ip_addresses: list[IPAddress] | None = None
    ip_ranges: list[IPRange] | None = None
    matching_target: str | None = None
    network_ids: list[str] | None = None
    regions: list[str] | None = None
    schedule: Schedule | None = None
    target_devices: list[TargetDevice] | None = None
