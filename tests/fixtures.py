"""Fixtures for different items from UniFi controller."""

from aiounifi.models.device import Device, HardwareCapability

TEST_DEVICE_1 = Device.from_json(
    {
        "_id": "B185CAFAEAEB81BD8ED2C4DE",
        "device_id": "595885953567485923",
        "name": "Test Device 1",
        "hw_caps": HardwareCapability.LED_RING,
        "port_table": [
            {"port_idx": 1},
            {"port_idx": 2},
            {"port_idx": 3},
            {"port_idx": 4},
        ],
        "outlet_table": [
            {
                "index": 1,
                "name": "Outlet 1",
            },
            {
                "index": 2,
                "name": "Outlet 2",
            },
            {
                "index": 3,
                "name": "Outlet 3",
            },
            {
                "index": 4,
                "name": "Outlet 4",
            },
        ],
    }
)


TEST_DEVICE_2 = Device.from_json(
    {
        "_id": "78E4C7550618938745CC27C3",
        "device_id": "834884606192757740",
        "name": "Test Device 2",
        "port_table": [
            {"port_idx": 1},
            {"port_idx": 2},
            {"port_idx": 3},
            {"port_idx": 4},
            {"port_idx": 5},
            {"port_idx": 6},
            {"port_idx": 7},
            {"port_idx": 8},
        ],
        "outlet_table": [
            {
                "index": 1,
                "name": "Outlet 1",
            },
            {
                "index": 2,
                "name": "Outlet 2",
            },
            {
                "index": 3,
                "name": "Outlet 3",
            },
            {
                "index": 4,
                "name": "Outlet 4",
            },
        ],
        "outlet_overrides": [
            {
                "index": 1,
                "name": "Outlet 1.1",
                "relay_state": False,
                "cycle_enabled": False,
            }
        ],
    }
)


TEST_DEVICE_3 = Device.from_json(
    {
        "_id": "7F7815F555B9783C4ABB52CF",
        "device_id": "A8FA0B014CB87BE0C2",
        "name": "Test Device 3",
        "hw_caps": HardwareCapability.LED_RING,
        "port_table": [
            {},
        ],
    }
)
