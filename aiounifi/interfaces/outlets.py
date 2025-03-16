"""Device outlet handler."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..models.device import Outlet
from .api_handlers import APIHandler, ItemEvent

if TYPE_CHECKING:
    from ..client import UnifiClient


class Outlets(APIHandler[Outlet]):
    """Represents network device ports."""

    item_cls = Outlet

    def __init__(self, controller: UnifiClient) -> None:
        """Initialize API handler."""
        super().__init__(controller)
        controller.devices.subscribe(self.process_device)

    def process_device(self, event: ItemEvent, obj_id: str) -> None:
        """Add, update, remove."""
        if event in (ItemEvent.ADDED, ItemEvent.CHANGED):
            device = self.client.devices[obj_id]
            for outlet in device.outlet_table:
                outlet_id = f"{obj_id}_{outlet.index}"
                self[outlet_id] = outlet
            return

        matched_obj_ids = [
            outlet_id for outlet_id in self if outlet_id.startswith(obj_id)
        ]
        for outlet_id in matched_obj_ids:
            self.pop(outlet_id)
