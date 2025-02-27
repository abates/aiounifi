"""Device outlet handler."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..models.device import Outlet
from .api_handlers import APIHandler, ItemEvent

if TYPE_CHECKING:
    from ..controller import Controller


class Outlets(APIHandler[Outlet]):
    """Represents network device ports."""

    item_cls = Outlet

    def __init__(self, controller: Controller) -> None:
        """Initialize API handler."""
        super().__init__(controller)
        controller.devices.subscribe(self.process_device)

    def process_device(self, event: ItemEvent, device_id: str) -> None:
        """Add, update, remove."""
        if event in (ItemEvent.ADDED, ItemEvent.CHANGED):
            device = self.controller.devices[device_id]
            for outlet in device.outlet_table:
                obj_id = f"{device_id}_{outlet.index}"
                self[obj_id] = outlet
            return

        matched_obj_ids = [obj_id for obj_id in self if obj_id.startswith(device_id)]
        for obj_id in matched_obj_ids:
            self.pop(obj_id)
