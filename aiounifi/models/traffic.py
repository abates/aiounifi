"""Data models related to IP traffic."""

from dataclasses import dataclass

from aiounifi.models.api import ApiItem


@dataclass
class PortRange(ApiItem):
    """Port range type definition."""

    port_start: int
    port_stop: int


@dataclass
class IPAddress(ApiItem):
    """IP Address for which traffic rule is applicable type definition."""

    ip_or_subnet: str
    ip_version: str
    port_ranges: list[PortRange]
    ports: list[int]


@dataclass
class IPRange(ApiItem):
    """IP Range type definition."""

    ip_start: str
    ip_stop: str
    ip_version: str


@dataclass
class TargetDevice(ApiItem):
    """Target device to which the routes and rules apply."""

    client_mac: str | None = None
    network_id: str | None = None
    type: str | None = None
