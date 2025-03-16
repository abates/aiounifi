"""DPI Restrictions as part of a UniFi network."""

from dataclasses import dataclass

from .api import ApiItem, json_field


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
