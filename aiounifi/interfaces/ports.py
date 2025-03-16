"""Device port handler."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..models.device import Port
from .api_handlers import APIHandler, ItemEvent

if TYPE_CHECKING:
    from ..client import UnifiClient


class Ports(APIHandler[Port]):
    """Represents network device ports."""

    item_cls = Port

    def __init__(self, controller: UnifiClient) -> None:
        """Initialize API handler."""
        super().__init__(controller)
        controller.devices.subscribe(self.process_device)

    def process_device(self, event: ItemEvent, obj_id: str) -> None:
        """Add, update, remove."""
        if event in (ItemEvent.ADDED, ItemEvent.CHANGED):
            device = self.client.devices[obj_id]
            for port in device.port_table:
                if (port_idx := port.port_idx or port.ifname) is None:
                    continue
                port_id = f"{obj_id}_{port_idx}"
                self[port_id] = port
            return

        matched_obj_ids = [port_id for port_id in self if port_id.startswith(obj_id)]
        for port_id in matched_obj_ids:
            self.pop(port_id)
