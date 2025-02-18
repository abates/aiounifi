"""DPI Restrictions as part of a UniFi network."""

from dataclasses import dataclass, field
from typing import Self

from .api import ApiItem, ApiRequest, json_field


@dataclass
class DpiRestrictionGroupListRequest(ApiRequest):
    """Request object for DPI restriction group list."""

    @classmethod
    def create(cls) -> Self:
        """Create DPI restriction group list request."""
        return cls(method="get", path="/rest/dpigroup")


@dataclass
class DPIRestrictionGroup(ApiItem):
    """DPI restriction group type definition."""

    id: str = json_field("_id")

    attr_no_delete: bool | None = None
    attr_hidden_id: str | None = None
    dpiapp_ids: list[str] = field(default_factory=list)
    name: str | None = None
    site_id: str | None = None
