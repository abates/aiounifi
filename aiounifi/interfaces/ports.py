"""Device port handler."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..models.device import Port
from .api_handlers import APIHandler, ItemEvent

if TYPE_CHECKING:
    from ..controller import Controller


class Ports(APIHandler[Port]):
    """Represents network device ports."""

    item_cls = Port

    def __init__(self, controller: Controller) -> None:
        """Initialize API handler."""
        super().__init__(controller)
        controller.devices.subscribe(self.process_device)

    def process_device(self, event: ItemEvent, device_id: str) -> None:
        """Add, update, remove."""
        if event in (ItemEvent.ADDED, ItemEvent.CHANGED):
            device = self.controller.devices[device_id]
            for port in device.port_table:
                if (port_idx := port.port_idx or port.ifname) is None:
                    continue
                obj_id = f"{device_id}_{port_idx}"
                self[obj_id] = port
            return

        matched_obj_ids = [obj_id for obj_id in self if obj_id.startswith(device_id)]
        for obj_id in matched_obj_ids:
            self.pop(obj_id)
