"""DPI Restrictions as part of a UniFi network."""

from dataclasses import dataclass, field

from .api import ApiItem, json_field


@dataclass
class DPIRestrictionGroup(ApiItem):
    """DPI restriction group type definition."""

    id: str = json_field("_id")

    attr_no_delete: bool | None = None
    attr_hidden_id: str | None = None
    dpiapp_ids: list[str] = field(default_factory=list)
    name: str | None = None
    site_id: str | None = None
