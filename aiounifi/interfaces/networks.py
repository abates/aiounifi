"""The security endpoint manages many things including firewall groups and rules."""

from ..models.networks import NetworkConf, NetworkConfRequest
from .api_handlers import APIHandler


class Networks(APIHandler[NetworkConf]):
    """Represents network configurations."""

    obj_id_key = "_id"
    item_cls = NetworkConf
    # process_messages = ()
    api_request = NetworkConfRequest.create()
