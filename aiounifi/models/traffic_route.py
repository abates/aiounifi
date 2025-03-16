"""Traffic routes as part of a UniFi network."""

from dataclasses import dataclass
from enum import StrEnum

from aiounifi.models.traffic import IPAddress, IPRange, PortRange, TargetDevice

from .api import ApiItem, json_field


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

    description: str | None = None
    domains: list[Domain] | None = None
    enabled: bool | None = None
    ip_addresses: list[IPAddress] | None = None
    ip_ranges: list[IPRange] | None = None
    matching_target: MatchingTarget | None = None
    network_id: str | None = None
    next_hop: str | None = None
    regions: list[str] | None = None
    target_devices: list[TargetDevice] | None = None
