"""DPI Restrictions as part of a UniFi network."""

from dataclasses import dataclass
from typing import Self

from .api import ApiItem, ApiRequest, json_field


@dataclass
class DPIRestrictionApp(ApiItem):
    """DPI restriction app type definition."""

    id: str = json_field("_id")
    apps: list[str] | None = None
    blocked: bool | None = None
    cats: list[str] | None = None
    enabled: bool | None = None
    log: bool | None = None
    site_id: str | None = None


@dataclass
class DpiRestrictionAppListRequest(ApiRequest):
    """Request object for DPI restriction app list."""

    @classmethod
    def create(cls) -> Self:
        """Create DPI restriction app list request."""
        return cls(method="get", path="/rest/dpiapp")


@dataclass
class DPIRestrictionAppEnableRequest(ApiRequest):
    """Request object for enabling DPI Restriction App."""

    @classmethod
    def create(cls, app_id: str, enable: bool) -> Self:
        """Create enabling DPI Restriction App request."""
        return cls(
            method="put",
            path=f"/rest/dpiapp/{app_id}",
            data={"enabled": enable},
        )
