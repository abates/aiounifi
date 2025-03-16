"""Site is a specific grouping in a UniFi network."""

from dataclasses import dataclass

from .api import ApiItem, json_field


@dataclass
class Site(ApiItem):
    """Site description."""

    site_id: str | None = json_field("_id", default=None)
    description: str | None = json_field("desc", default=None)
    hidden_id: str | None = json_field("attr_hidden_id", default=None)
    name: str | None = None
    no_delete: bool | None = json_field("attr_no_delete", default=None)
    role: str | None = None
