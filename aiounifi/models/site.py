"""Site is a specific grouping in a UniFi network."""

from dataclasses import dataclass
from typing import Self

from .api import ApiItem, ApiRequest, json_field


@dataclass
class Site(ApiItem):
    """Site description."""

    site_id: str | None = json_field("_id", default=None)
    description: str | None = json_field("desc", default=None)
    hidden_id: str | None = json_field("attr_hidden_id", default=None)
    name: str | None = None
    no_delete: bool | None = json_field("attr_no_delete", default=None)
    role: str | None = None


@dataclass
class SiteListRequest(ApiRequest):
    """Request object for site list."""

    @classmethod
    def create(cls) -> Self:
        """Create site list request."""
        return cls(method="get", path="/self/sites")

    def full_path(self, site: str, is_unifi_os: bool) -> str:
        """Url to list sites is global for controller."""
        if is_unifi_os:
            return f"/proxy/network/api{self.path}"
        return f"/api{self.path}"
