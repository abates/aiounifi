"""The security endpoint manages many things including firewall groups and rules."""

from typing import Any

from ..models.networks import (
    CorporateNetworkConf,
    NetworkConf,
    NetworkConfRequest,
    WanNetworkConf,
)
from .api_handlers import APIHandler


class Networks(APIHandler[NetworkConf]):
    """Represents network configurations."""

    obj_id_key = "_id"
    # process_messages = ()
    api_request = NetworkConfRequest()

    def process_item(self, raw: dict[str, Any]):
        """Process the item and add a CorporateNetworkConf or WanNetworkConf object to the handler."""
        if "purpose" in raw:
            if raw["purpose"] == "corporate":
                self[raw[self.obj_id_key]] = CorporateNetworkConf.from_json(data=raw)
                return
            elif raw["purpose"] == "wan":
                self[raw[self.obj_id_key]] = WanNetworkConf.from_json(data=raw)
                return
        raise ValueError(
            f"Cannot process network conf with purpose {raw.get('purpose')}"
        )
