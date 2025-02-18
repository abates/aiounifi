"""Traffic routes as part of a UniFi network."""

from dataclasses import dataclass
from enum import StrEnum
from typing import Self

from aiounifi.models.traffic import IPAddress, IPRange, PortRange, TargetDevice

from .api import ApiItem, ApiRequestV2, json_field


class MatchingTarget(StrEnum):
    """Possible matching targets for a traffic rule."""

    DOMAIN = "DOMAIN"
    IP = "IP"
    INTERNET = "INTERNET"
    REGION = "REGION"


@dataclass
class Domain(ApiItem):
    """A target domain for a traffic route."""

    domain: str
    port_ranges: list[PortRange]
    ports: list[int]


@dataclass
class TrafficRoute(ApiItem):
    """Traffic route type definition."""

    id: str = json_field("_id")
    description: str
    domains: list[Domain]
    enabled: bool
    ip_addresses: list[IPAddress]
    ip_ranges: list[IPRange]
    matching_target: MatchingTarget
    network_id: str
    next_hop: str
    regions: list[str]
    target_devices: list[TargetDevice]


@dataclass
class TrafficRouteListRequest(ApiRequestV2):
    """Request object for traffic route list."""

    @classmethod
    def create(cls) -> Self:
        """Create traffic route request."""
        return cls(method="get", path="/trafficroutes", data=None)


@dataclass
class TrafficRouteSaveRequest(ApiRequestV2):
    """Request object for saving a traffic route.

    To modify a route, you must make sure the `raw` attribute of the TypedTrafficRoute is modified.
    The properties provide convient access for reading, however do not provide means of setting values.
    """

    @classmethod
    def create(cls, traffic_route: TrafficRoute, enable: bool | None = None) -> Self:
        """Create traffic route save request."""
        if enable is not None:
            traffic_route["enabled"] = enable
        return cls(
            method="put",
            path=f"/trafficroutes/{traffic_route['_id']}",
            data=traffic_route,
        )
