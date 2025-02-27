"""DPI Restrictions as part of a UniFi network."""

from dataclasses import dataclass

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

    def __init__(self):
        """Create DPI restriction app list request."""
        super().__init__(method="get", path="/rest/dpiapp")


@dataclass
class DPIRestrictionAppEnableRequest(ApiRequest):
    """Request object for enabling DPI Restriction App."""

    def __init__(self, app_id: str, enable: bool):
        """Create enabling DPI Restriction App request."""
        super().__init__(
            method="put",
            path=f"/rest/dpiapp/{app_id}",
            data={"enabled": enable},
        )
