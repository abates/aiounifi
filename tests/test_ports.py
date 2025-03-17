"""Test aioUniFi device ports."""

from unittest.mock import Mock

from aiounifi.interfaces.api_handlers import ItemEvent
from aiounifi.interfaces.ports import Ports

from tests.fixtures import TEST_DEVICE_1, TEST_DEVICE_2, TEST_DEVICE_3


def test_process_device():
    """Verify the `process_device` callback correctly manipulates ports."""
    devices = {
        TEST_DEVICE_1.device_id: TEST_DEVICE_1,
        TEST_DEVICE_2.device_id: TEST_DEVICE_2,
        TEST_DEVICE_3.device_id: TEST_DEVICE_3,
    }
    client = Mock()
    client.devices = Mock()
    client.devices.__getitem__ = Mock(side_effect=lambda key: devices[key])

    ports = Ports(client)
    assert len(ports) == 0

    ports.process_device(ItemEvent.ADDED, TEST_DEVICE_1.device_id)
    assert len(ports) == 4
    for port in TEST_DEVICE_1.port_table:
        obj_id = f"{TEST_DEVICE_1.device_id}_{port.port_idx}"
        assert ports[obj_id] == port

    ports.process_device(ItemEvent.ADDED, TEST_DEVICE_2.device_id)
    assert len(ports) == 12
    for device in [TEST_DEVICE_1, TEST_DEVICE_2]:
        for port in device.port_table:
            obj_id = f"{device.device_id}_{port.port_idx}"
            assert ports[obj_id] == port

    ports.process_device(ItemEvent.DELETED, TEST_DEVICE_1.device_id)
    assert len(ports) == len(TEST_DEVICE_2.port_table)
    for port in TEST_DEVICE_2.port_table:
        obj_id = f"{TEST_DEVICE_2.device_id}_{port.port_idx}"
        assert ports[obj_id] == port

    # TEST_DEVICE_3 ports have no names/ids, so nothing should be added
    ports.process_device(ItemEvent.ADDED, TEST_DEVICE_3.device_id)
    assert len(ports) == 8
