"""Test aioUniFi device outlets.

pytest --cov-report term-missing --cov=aiounifi.outlets tests/test_outlets.py
"""

from unittest.mock import Mock

from aiounifi.interfaces.api_handlers import ItemEvent
from aiounifi.interfaces.outlets import Outlets

from .fixtures import TEST_DEVICE_1, TEST_DEVICE_2


def test_outlets_handler_device_processing():
    """Verify that outlets are managed as device signals are received."""
    devices = {}
    outlets = {}
    for device in [TEST_DEVICE_1, TEST_DEVICE_2]:
        devices[device.device_id] = device
        for outlet in device.outlet_table:
            outlets[f"{device.device_id}_{outlet.index}"] = outlet
    assert len(outlets) == 8
    controller = Mock()
    controller.devices = Mock()
    controller.devices.__getitem__ = Mock(side_effect=lambda key: devices[key])
    handler = Outlets(controller)

    for device_id in devices:
        handler.process_device(ItemEvent.ADDED, device_id)
    assert handler.data == outlets

    outlets = {
        outlet_id: outlet
        for outlet_id, outlet in outlets.items()
        if not outlet_id.startswith(TEST_DEVICE_2.device_id)
    }

    handler.process_device(ItemEvent.DELETED, TEST_DEVICE_2.device_id)
    assert handler.data == outlets

    handler.process_device(ItemEvent.CHANGED, TEST_DEVICE_1.device_id)
    assert handler.data == outlets
