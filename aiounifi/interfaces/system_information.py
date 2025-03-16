"""System information of a UniFi network."""

from aiounifi.models.api import ApiEndpoint

from ..models.system_information import SystemInformation
from .api_handlers import APIHandler


class SystemInformationHandler(APIHandler[SystemInformation]):
    """Represents system information interface."""

    obj_id_key = "anonymous_controller_id"
    item_cls = SystemInformation
    list_endpoint = ApiEndpoint(path="/stat/sysinfo")
