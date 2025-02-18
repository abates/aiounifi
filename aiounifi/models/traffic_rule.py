"""Traffic rules as part of a UniFi network."""

from dataclasses import dataclass
from typing import Self

from aiounifi.models.traffic import IPAddress, IPRange, TargetDevice

from .api import ApiItem, ApiRequestV2, json_field


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
    action: str
    app_category_ids: list[str]
    app_ids: list[str]
    bandwidth_limit: BandwidthLimit
    description: str
    domains: list[str]
    enabled: bool
    ip_addresses: list[IPAddress]
    ip_ranges: list[IPRange]
    matching_target: str
    network_ids: list[str]
    regions: list[str]
    schedule: Schedule
    target_devices: list[TargetDevice]


@dataclass
class TrafficRuleListRequest(ApiRequestV2):
    """Request object for traffic rule list."""

    @classmethod
    def create(cls) -> Self:
        """Create traffic rule request."""
        return cls(method="get", path="/trafficrules", data=None)


@dataclass
class TrafficRuleEnableRequest(ApiRequestV2):
    """Request object for traffic rule enable."""

    @classmethod
    def create(cls, traffic_rule: TrafficRule, enable: bool) -> Self:
        """Create traffic rule enable request."""
        traffic_rule["enabled"] = enable
        return cls(
            method="put",
            path=f"/trafficrules/{traffic_rule['_id']}",
            data=traffic_rule,
        )
