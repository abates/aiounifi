"""UniFi sites of network infrastructure."""

from aiounifi.models.api import Endpoint

from ..models.site import Site
from .api_handlers import APIHandler


class Sites(APIHandler[Site]):
    """Represent UniFi sites."""

    obj_id_key = "_id"
    item_cls = Site
    list_endpoint = Endpoint(path="/self/sites")
