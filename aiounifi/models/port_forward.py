"""Port forwarding in a UniFi network."""

from dataclasses import dataclass

from .api import ApiItem, ApiRequest, json_field


@dataclass
class PortForward(ApiItem):
    """Represents a port forward configuration."""

    id: str | None = json_field("_id", default=None)
    destination_port: str | None = json_field("dst_port", default=None)
    enabled: bool | None = None
    forward_port: str | None = json_field("fwd_port", default=None)
    forward_ip: str | None = json_field("fwd", default=None)
    name: str | None = None
    port_forward_interface: str | None = json_field("pfwd_interface", default=None)
    protocol: str | None = json_field("proto", default=None)
    site_id: str | None = None
    source: str | None = json_field("src", default=None)


@dataclass
class PortForwardListRequest(ApiRequest):
    """Request object for port forward list."""

    def __init__(self):
        """Create port forward list request."""
        super().__init__(method="get", path="/rest/portforward")


@dataclass
class PortForwardEnableRequest(ApiRequest):
    """Request object for enabling port forward."""

    def __init__(self, port_forward: "PortForward", enable: bool):
        """Create enable port forward request."""
        data = (port_forward.raw or {}).copy()
        data["enabled"] = enable
        super().__init__(
            method="put",
            path=f"/rest/portforward/{data['_id']}",
            data=data,
        )
