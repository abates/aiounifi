"""Use aiounifi as a CLI."""

import argparse
import asyncio
from asyncio.timeouts import timeout
import logging
from ssl import SSLContext

import aiohttp

import aiounifi
from aiounifi.client import UnifiClient
from aiounifi.models.configuration import Configuration

LOGGER = logging.getLogger(__name__)


async def unifi_controller(
    host: str,
    username: str,
    password: str,
    port: int,
    site: str,
    session: aiohttp.ClientSession,
    ssl_context: SSLContext | None = None,
) -> UnifiClient | None:
    """Set up UniFi controller and verify credentials."""
    controller = UnifiClient(
        Configuration(
            session,
            host,
            username=username,
            password=password,
            port=port,
            site=site,
            ssl_context=ssl_context if ssl_context is not None else False,
        )
    )

    try:
        async with timeout(10):
            await controller.login()
        return controller

    except aiounifi.LoginRequired:
        LOGGER.warning("Connected to UniFi at %s but couldn't log in", host)

    except aiounifi.Unauthorized:
        LOGGER.warning("Connected to UniFi at %s but not registered", host)

    except (TimeoutError, aiounifi.RequestError):
        LOGGER.exception("Error connecting to the UniFi controller at %s", host)

    except aiounifi.AiounifiException:
        LOGGER.exception("Unknown UniFi communication error occurred")

    return None


async def main(
    host: str,
    username: str,
    password: str,
    port: int,
    site: str,
    ssl_context: SSLContext | None = None,
) -> None:
    """CLI method for library."""
    LOGGER.info("Starting aioUniFi")

    websession = aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar(unsafe=True))

    controller = await unifi_controller(
        host=host,
        username=username,
        password=password,
        port=port,
        site=site,
        session=websession,
        ssl_context=ssl_context,
    )

    if not controller:
        LOGGER.error("Couldn't connect to UniFi controller")
        await websession.close()
        return

    await asyncio.gather(
        *(
            controller.clients.update(),
            controller.clients_all.update(),
            controller.devices.update(),
            controller.dpi_apps.update(),
            controller.dpi_groups.update(),
            controller.firewall_address_groups.update(),
            controller.firewall_port_groups.update(),
            controller.firewall_rules.update(),
            controller.firewall_rules.update(),
            controller.port_forwarding.update(),
            controller.sites.update(),
            controller.system_information.update(),
            controller.traffic_rules.update(),
            controller.traffic_routes.update(),
            controller.vouchers.update(),
            controller.wlans.update(),
        ),
        return_exceptions=True,
    )

    ws_task = asyncio.create_task(controller.start_websocket())

    try:
        while True:
            await asyncio.sleep(1)

    except asyncio.CancelledError:
        pass

    finally:
        ws_task.cancel()
        await websession.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("host", type=str)
    parser.add_argument("username", type=str)
    parser.add_argument("password", type=str)
    parser.add_argument("-p", "--port", type=int, default=8443)
    parser.add_argument("-s", "--site", type=str, default="default")
    parser.add_argument("-D", "--debug", action="store_true")
    args = parser.parse_args()

    LOG_LEVEL = logging.INFO
    if args.debug:
        LOG_LEVEL = logging.DEBUG
    logging.basicConfig(format="%(message)s", level=LOG_LEVEL)

    LOGGER.info(
        "%s, %s, %s, %i, %s",
        args.host,
        args.username,
        args.password,
        args.port,
        args.site,
    )

    try:
        asyncio.run(
            main(
                host=args.host,
                username=args.username,
                password=args.password,
                port=args.port,
                site=args.site,
            )
        )
    except KeyboardInterrupt:
        LOGGER.info("Keyboard interrupt")
