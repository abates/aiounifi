"""Python library to interact with UniFi controller."""

from __future__ import annotations

import datetime
from functools import wraps
from http import HTTPStatus
import logging
from typing import Any

import aiohttp

from aiounifi import errors
from aiounifi.models.api import ApiEndpoint, ApiItem, ApiResponse, Endpoint

from .interfaces.clients import Clients
from .interfaces.clients_all import ClientsAll
from .interfaces.devices import Devices
from .interfaces.dpi_restriction_apps import DPIRestrictionApps
from .interfaces.dpi_restriction_groups import DPIRestrictionGroups
from .interfaces.events import EventHandler
from .interfaces.messages import MessageHandler
from .interfaces.networks import Networks
from .interfaces.outlets import Outlets
from .interfaces.port_forwarding import PortForwarding
from .interfaces.ports import Ports
from .interfaces.security import (
    FirewallAddressGroups,
    FirewallPortGroups,
    FirewallRules,
)
from .interfaces.sites import Sites
from .interfaces.system_information import SystemInformationHandler
from .interfaces.traffic_routes import TrafficRoutes
from .interfaces.traffic_rules import TrafficRules
from .interfaces.vouchers import Vouchers
from .interfaces.wlans import Wlans
from .models.configuration import Configuration

LOGGER = logging.getLogger(__name__)


def check_session(func):
    """Confirm the client session is not None."""

    @wraps(func)
    def wrapper(self: UnifiClient, *args, **kwargs):
        if not hasattr(self, "session") or self.session is None:
            raise errors.NotConnectedError(
                "Client is not yet connected to the controller."
            )
        return func(self, *args, **kwargs)

    return wrapper


class UnifiClient:
    """Control a UniFi controller."""

    session: aiohttp.ClientSession

    def __init__(self, config: Configuration) -> None:
        """Session setup."""
        self.config = config
        self._is_unifi_os: bool | None = None

        self.messages = MessageHandler(self)
        self.events = EventHandler(self)

        self.clients = Clients(self)
        self.clients_all = ClientsAll(self)
        self.devices = Devices(self)
        self.firewall_address_groups = FirewallAddressGroups(self)
        self.firewall_port_groups = FirewallPortGroups(self)
        self.firewall_rules = FirewallRules(self)
        self.networks = Networks(self)
        self.outlets = Outlets(self)
        self.ports = Ports(self)
        self.dpi_apps = DPIRestrictionApps(self)
        self.dpi_groups = DPIRestrictionGroups(self)
        self.port_forwarding = PortForwarding(self)
        self.sites = Sites(self)
        self.system_information = SystemInformationHandler(self)
        self.traffic_rules = TrafficRules(self)
        self.traffic_routes = TrafficRoutes(self)
        self.vouchers = Vouchers(self)
        self.wlans = Wlans(self)

    async def connect(self) -> None:
        """Check if controller is running UniFi OS."""
        self.session = aiohttp.ClientSession(raise_for_status=errors.raise_for_status)
        # We have to set `allow_redirects` to False here because the redirect
        # is what is used to detect new-style API or old-style API. A 200 response
        # uses the new API paths, where a 302 is older controllers.
        response = await self.session.get(
            self.config.url, allow_redirects=False, ssl=self.config.ssl_context
        )
        if response.status == HTTPStatus.OK:
            self._is_unifi_os = True
            self.session.cookie_jar.clear_domain(self.config.host)
        elif response.status == HTTPStatus.FOUND:
            self._is_unifi_os = False
        else:
            await self.session.close()
            delattr(self, "session")
            raise errors.AiounifiException(
                f"Could not determine if controller is unifi os. Got HTTP status {response.status}"
            )
        LOGGER.debug("Talking to UniFi OS device: %s", self._is_unifi_os)

    @check_session
    async def login(self) -> None:
        """Log in to controller."""

        self.session.headers.clear()
        url = f"{self.config.url}/api{'/auth/login' if self.is_unifi_os else '/login'}"

        auth = {
            "username": self.config.username,
            "password": self.config.password,
            "rememberMe": True,
        }

        response = await self.session.post(url, json=auth)
        if response.content_type != "application/json":
            LOGGER.debug("Login Failed not JSON: '%s'", await response.read())
            raise errors.RequestError("Login Failed: Host starting up")

        data = await response.json()
        errors.raise_for_unifi_error(1, data)

        if (csrf_token := response.headers.get("x-csrf-token")) is not None:
            self.session.headers["x-csrf-token"] = csrf_token

        LOGGER.debug("Logged in to UniFi %s", url)

    @property
    def is_unifi_os(self):
        """Indite whether or not this client connection is to a Unifi OS device."""
        if self._is_unifi_os is None:
            raise errors.NotConnectedError(
                "Client is not yet connected to the controller."
            )
        return self._is_unifi_os

    async def get(
        self, endpoint: Endpoint, api_item: ApiItem | None = None
    ) -> ApiResponse:
        """Perform an API request using the GET method.

        Args:
            endpoint (Endpoint): The endpoint to call.
            api_item (ApiItem | None, optional): Optional item to pass to the `endpoint.format`
                method. Defaults to None.

        Returns:
            ApiResponse: The processed ApiResponse.

        """

        return await self.endpoint_request(
            method="get", endpoint=endpoint, api_item=api_item
        )

    async def post(
        self, endpoint: Endpoint, api_item: ApiItem | None, data: dict[str, Any]
    ) -> ApiResponse:
        """Perform an API request using the POST method.

        Args:
            endpoint (Endpoint): The endpoint to call.
            api_item (ApiItem | None, optional): Optional item to pass to the `endpoint.format`
                method. Defaults to None.
            data (dict[str, Any]): Any data to be marshaled to JSON and sent with the POST request.

        Returns:
            ApiResponse: The processed ApiResponse.

        """

        return await self.endpoint_request(
            method="post", endpoint=endpoint, api_item=api_item, data=data
        )

    async def put(
        self, endpoint: Endpoint, api_item: ApiItem | None, data: dict[str, Any]
    ) -> ApiResponse:
        """Perform an API request using the PUT method.

        Args:
            endpoint (Endpoint): The endpoint to call.
            api_item (ApiItem | None, optional): Optional item to pass to the `endpoint.format`
                method. Defaults to None.
            data (dict[str, Any]): Any data to be marshaled to JSON and sent with the POST request.

        Returns:
            ApiResponse: The processed ApiResponse.

        """

        return await self.endpoint_request(
            method="put", endpoint=endpoint, api_item=api_item, data=data
        )

    @check_session
    async def endpoint_request(
        self,
        method: str,
        endpoint: Endpoint,
        api_item: ApiItem | None = None,
        data: dict[str, Any] | None = None,
    ) -> ApiResponse:
        """Handle generic API requests."""
        url = endpoint.format(site=self.config.site, api_item=api_item)
        request_args = {
            "method": method,
            "url": url,
            "json": data,
            "ssl": self.config.ssl_context,
        }
        try:
            async with self.session.request(**request_args) as response:
                response_data = await response.json() if response.status != 204 else {}
        except errors.LoginRequired:
            # Session likely expired, try again
            await self.login()
            async with self.session.request(**request_args) as response:
                response_data = await response.json() if response.status != 204 else {}

        if isinstance(endpoint, ApiEndpoint):
            errors.raise_for_unifi_error(endpoint.version, response_data)
        return ApiResponse(**response_data)

    @check_session
    async def start_websocket(self) -> None:
        """Run the websocket listener loop.

        Note: This method will not return so long as the websocket is connected. Therefore,
        it should be started in its own coroutine.
        """
        url = f"wss://{self.config.host}:{self.config.port}"
        url += "/proxy/network" if self.is_unifi_os else ""
        url += f"/wss/s/{self.config.site}/events"

        try:
            async with self.session.ws_connect(
                url,
                ssl=self.config.ssl_context,
                heartbeat=15,
                compress=12,
            ) as websocket_connection:
                LOGGER.debug(
                    "Connected to UniFi websocket %s, headers: %s, cookiejar: %s",
                    url,
                    self.session.headers,
                    self.session.cookie_jar._cookies,  # type: ignore[attr-defined]
                )
                async for message in websocket_connection:
                    self.ws_message_received = datetime.datetime.now(datetime.UTC)

                    if message.type is aiohttp.WSMsgType.TEXT:
                        LOGGER.debug("Websocket '%s'", message.data)
                        self.messages.new_data(message.data)

                    elif message.type is aiohttp.WSMsgType.CLOSED:
                        LOGGER.warning(
                            "Connection closed to UniFi websocket '%s'", message.data
                        )
                        break

                    elif message.type is aiohttp.WSMsgType.ERROR:
                        LOGGER.error("UniFi websocket error: '%s'", message.data)
                        raise errors.WebsocketError(message.data)

                    else:
                        LOGGER.warning(
                            "Unexpected websocket message type '%s' with data '%s'",
                            message.type,
                            message.data,
                        )

        except aiohttp.ClientConnectorError as err:
            LOGGER.error("Error connecting to UniFi websocket: '%s'", err)
            err.add_note("Error connecting to UniFi websocket")
            raise

        except aiohttp.WSServerHandshakeError as err:
            LOGGER.error(
                "Server handshake error connecting to UniFi websocket: '%s'", err
            )
            err.add_note("Server handshake error connecting to UniFi websocket")
            raise

        except errors.WebsocketError:
            raise

        except Exception as err:
            LOGGER.exception(err)
            raise errors.WebsocketError from err
