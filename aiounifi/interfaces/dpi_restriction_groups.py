"""DPI Restrictions as part of a UniFi network."""

from aiounifi.models.api import ApiEndpoint

from ..models.dpi_restriction_group import DPIRestrictionGroup
from ..models.message import MessageKey
from .api_handlers import APIHandler


class DPIRestrictionGroups(APIHandler[DPIRestrictionGroup]):
    """Represents DPI Group configurations."""

    obj_id_key = "_id"
    item_cls = DPIRestrictionGroup
    process_messages = (MessageKey.DPI_GROUP_ADDED, MessageKey.DPI_GROUP_UPDATED)
    remove_messages = (MessageKey.DPI_GROUP_REMOVED,)
    list_endpoint = ApiEndpoint(path="/rest/dpigroup")
