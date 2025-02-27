"""Traffic rules as part of a UniFi network."""

from ..models.api import ApiResponse
from ..models.traffic_rule import (
    TrafficRule,
    TrafficRuleEnableRequest,
    TrafficRuleListRequest,
)
from .api_handlers import APIHandler


class TrafficRules(APIHandler[TrafficRule]):
    """Represents TrafficRules configurations."""

    obj_id_key = "_id"
    item_cls = TrafficRule
    api_request = TrafficRuleListRequest()

    async def enable(self, traffic_rule: TrafficRule) -> ApiResponse:
        """Enable traffic rule defined in controller."""
        return await self.toggle(traffic_rule, state=True)

    async def disable(self, traffic_rule: TrafficRule) -> ApiResponse:
        """Disable traffic rule defined in controller."""
        return await self.toggle(traffic_rule, state=False)

    async def toggle(self, traffic_rule: TrafficRule, state: bool) -> ApiResponse:
        """Set traffic rule - defined in controller - to the desired state."""
        traffic_rule_response = await self.controller.request(
            TrafficRuleEnableRequest(traffic_rule, enable=state)
        )
        self.process_raw(traffic_rule_response.data)
        return traffic_rule_response
