"""Clients are devices on a UniFi network."""

from aiounifi.models.api import ApiEndpoint

from ..models.client import Client
from .api_handlers import APIHandler


class ClientsAll(APIHandler[Client]):
    """Represents all client network devices."""

    obj_id_key = "mac"
    item_cls = Client
    list_endpoint = ApiEndpoint(path="/rest/user")
