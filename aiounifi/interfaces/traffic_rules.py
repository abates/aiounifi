"""Traffic rules as part of a UniFi network."""

from ..models.api import ApiEndpoint, ApiResponse
from ..models.traffic_rule import TrafficRule
from .api_handlers import APIHandler


class TrafficRules(APIHandler[TrafficRule]):
    """Represents TrafficRules configurations."""

    obj_id_key = "_id"
    item_cls = TrafficRule
    list_endpoint = ApiEndpoint(path="/trafficrules", version=2)
    update_endpoint = ApiEndpoint(path="/trafficrules/{api_item.id}", version=2)

    async def enable(self, traffic_rule: TrafficRule) -> ApiResponse:
        """Enable traffic rule defined in controller."""
        traffic_rule.enabled = True
        return await self.save(traffic_rule)

    async def disable(self, traffic_rule: TrafficRule) -> ApiResponse:
        """Disable traffic rule defined in controller."""
        traffic_rule.enabled = False
        return await self.save(traffic_rule)
