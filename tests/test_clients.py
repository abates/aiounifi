"""Test client configuration API.

pytest --cov-report term-missing --cov=aiounifi.clients tests/test_clients.py
"""

from aioresponses import aioresponses
import pytest

from aiounifi.controller import Controller

from tests.conftest import UnifiCalledWith


@pytest.mark.parametrize(
    ("method", "mac", "command"),
    [
        ("block", "0", {"mac": "0", "cmd": "block-sta"}),
        ("unblock", "0", {"mac": "0", "cmd": "unblock-sta"}),
        ("reconnect", "0", {"mac": "0", "cmd": "kick-sta"}),
        ("remove_clients", ["0"], {"macs": ["0"], "cmd": "forget-sta"}),
    ],
)
async def test_client_commands(
    mock_aioresponse: aioresponses,
    unifi_controller: Controller,
    unifi_called_with: UnifiCalledWith,
    method: str,
    mac: str | list[str],
    command: dict[str, str | list[str]],
) -> None:
    """Test client commands."""
    mock_aioresponse.post("https://host:8443/api/s/default/cmd/stamgr", payload={})
    class_command = getattr(unifi_controller.clients, method)
    await class_command(mac)
    assert unifi_called_with("post", "/api/s/default/cmd/stamgr", json=command)
