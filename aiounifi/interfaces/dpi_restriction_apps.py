"""DPI Restrictions as part of a UniFi network."""

from ..models.api import ApiEndpoint, ApiResponse
from ..models.dpi_restriction_app import DPIRestrictionApp
from ..models.message import MessageKey
from .api_handlers import APIHandler


class DPIRestrictionApps(APIHandler[DPIRestrictionApp]):
    """Represents DPI App configurations."""

    obj_id_key = "_id"
    item_cls = DPIRestrictionApp
    process_messages = (MessageKey.DPI_APP_ADDED, MessageKey.DPI_APP_UPDATED)
    remove_messages = (MessageKey.DPI_APP_REMOVED,)
    list_endpoint = ApiEndpoint(path="/rest/dpiapp")
    update_endpoint = ApiEndpoint(path="/rest/dpiapp/{app_id}")

    async def enable(self, app: DPIRestrictionApp) -> ApiResponse:
        """Enable DPI Restriction Group Apps."""
        return await self.set_enabled(app, True)

    async def disable(self, app: DPIRestrictionApp) -> ApiResponse:
        """Disable DPI Restriction Group Apps."""
        return await self.set_enabled(app, False)

    async def set_enabled(self, app: DPIRestrictionApp, enabled: bool) -> ApiResponse:
        """Set the `enabled` value for a dpi app."""
        app.enabled = enabled
        return await self.save(app, {"enabled"})
