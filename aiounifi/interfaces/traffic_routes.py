"""Traffic routes as part of a UniFi network."""

from ..models.api import ApiEndpoint, ApiResponse
from ..models.traffic_route import TrafficRoute
from .api_handlers import APIHandler


class TrafficRoutes(APIHandler[TrafficRoute]):
    """Represents TrafficRoutes configurations."""

    obj_id_key = "_id"
    item_cls = TrafficRoute
    list_endpoint = ApiEndpoint(path="/trafficroutes", version=2)
    update_endpoint = ApiEndpoint(path="/trafficroutes/{api_item.id}", version=2)

    async def enable(self, traffic_route: TrafficRoute) -> ApiResponse:
        """Enable traffic route defined in controller."""
        traffic_route.enabled = True
        return await self.save(traffic_route)

    async def disable(self, traffic_route: TrafficRoute) -> ApiResponse:
        """Disable traffic route defined in controller."""
        traffic_route.enabled = False
        return await self.save(traffic_route)
