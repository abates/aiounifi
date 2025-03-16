"""Test wlan configuration API.

pytest --cov-report term-missing --cov=aiounifi.wlan tests/test_wlans.py
"""

from typing import Any

import pytest

from aiounifi.interfaces.wlans import Wlans
from aiounifi.models.wlan import Wlan

from tests.conftest import assert_handler_request


@pytest.mark.parametrize(
    ("method_name", "method_args", "expected_request", "expected_error"),
    [
        (
            "set_enabled",
            {
                "wlan": Wlan(id="wlan_id"),
                "enabled": True,
            },
            {
                "method": "put",
                "endpoint": Wlans.update_endpoint,
                "api_item": Wlan(id="wlan_id", enabled=True),
                "data": {
                    "enabled": True,
                },
            },
            None,
        ),
        (
            "enable",
            {
                "wlan": Wlan(id="wlan_id", enabled=False),
            },
            {
                "method": "put",
                "endpoint": Wlans.update_endpoint,
                "api_item": Wlan(id="wlan_id", enabled=True),
                "data": {
                    "enabled": True,
                },
            },
            None,
        ),
        (
            "disable",
            {
                "wlan": Wlan(id="wlan_id", enabled=True),
            },
            {
                "method": "put",
                "endpoint": Wlans.update_endpoint,
                "api_item": Wlan(id="wlan_id", enabled=False),
                "data": {
                    "enabled": False,
                },
            },
            None,
        ),
    ],
)
async def test_wlans(
    method_name: str,
    method_args: dict[str, Any],
    expected_request: dict[str, Any],
    expected_error: type[Exception] | None,
):
    """Test device interface methods."""
    await assert_handler_request(
        Wlans,
        method_name,
        method_args,
        expected_request,
        expected_error,
    )


def test_wlan_qr_code():
    """Test that wlan can be enabled and disabled."""
    wlan = Wlan(id="wlan_id", name="ssid", x_passphrase="passphrase", wpa_mode="wpa")
    assert wlan.generate_qr_code() == (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x84\x00\x00\x00"
        b"\x84\x01\x00\x00\x00\x00y?\xbe\n\x00\x00\x00\xc4IDATx\xda\xedV\xcb"
        b"\r\xc3P\x0cB]\xc0\xfbo\xc9\x06\x14\xfcri\x0fUUz\x8c\xf3\xd1\x93\xa5"
        b" \x8c\xb1\x15\xe8-\x88;\xf3\x9a\x010\x1cir\x10\x1fx\x8fo2\xc6\t\x84"
        b"\x86\xd7\xa1\xc0\xc1\x0c\x91\xb7\xef\x12\x07\xe1\xf2\x07\x9c\x81\xa6"
        b"\xc6\xd1\xaac\xa0N\x9f\xb4i\xa3\xec\xd7F\xc8\x1c'\xfc\xce\xe7\xb8H"
        b"\xe7)p\\LB\xe8t>U\x81\xeb\xa2\x02\x87\x80\xb9\x0c\x99\xbb\xe9;\x07V"
        b"\xc8 \x8bZ\xe8c\xf7D\x1djJ>\t\xee\xd5\xe0\xf8\xe3\xdd\x1a.L\xd5|\xb9M{"
        b"\x9e\xda\xcff\xe2\x9a:\x9c%\xc2k\xe8\xcby\xdf\xa5!\xf4\xfb\xd0^\x8eL5"
        b"\x0e\xd7\xd7\xa3\x9e\xcf\x8eG\xabO\xbcc\x8d\xfa}\x98\xbe\xb3\xdb\xab"
        b"\xf7_\xc1\x87\xcc\x13u:\xfe\x00\xeaq\xcby\x00\x00\x00\x00IEND\xaeB`\x82"
    )
