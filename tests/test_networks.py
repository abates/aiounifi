"""Test client configuration API.

pytest --cov-report term-missing --cov=aiounifi.devices tests/test_devices.py
"""

from unittest.mock import Mock

import pytest

from aiounifi.interfaces.networks import Networks
from aiounifi.models.networks import CorporateNetworkConf, WanNetworkConf


@pytest.mark.parametrize(
    ("input", "expected", "expected_error"),
    [
        (
            [{"_id": "corporate_id", "purpose": "corporate"}],
            [CorporateNetworkConf(_id="corporate_id", purpose="corporate")],
            None,
        ),
        (
            [{"_id": "wan_id", "purpose": "wan"}],
            [WanNetworkConf(_id="wan_id", purpose="wan")],
            None,
        ),
        (
            [{"_id": "other_id", "purpose": "other"}],
            [],
            ValueError,
        ),
    ],
)
def test_process_item(input, expected, expected_error):
    """Test all of the __repr__ methods."""
    controller = Mock()
    networks = Networks(controller)
    if expected_error:
        with pytest.raises(expected_error):
            networks.process_raw(input)
        assert list(networks.values()) == []
    else:
        networks.process_raw(input)
        assert list(networks.values()) == expected
