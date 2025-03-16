"""UniFi devices are network infrastructure.

Access points, gateways, power plugs, switches.
"""

from collections.abc import Sequence
import re
from typing import cast

from ..models.api import ApiEndpoint, ApiResponse
from ..models.device import Device, DeviceOutletOverrides, DevicePortOverrides
from ..models.message import MessageKey
from .api_handlers import APIHandler


def _merge_overrides(
    existing_overrides: Sequence[DeviceOutletOverrides | DevicePortOverrides],
    new_overrides: Sequence[DeviceOutletOverrides | DevicePortOverrides],
    index_attr: str,
):
    merged_overrides: list[DeviceOutletOverrides | DevicePortOverrides] = []
    sorted_overrides = sorted(
        new_overrides, key=lambda override: getattr(override, index_attr)
    )
    for override in existing_overrides:
        existing_index = getattr(override, index_attr)
        if sorted_overrides:
            new_index = getattr(sorted_overrides[0], index_attr)
            if existing_index == new_index:
                merged_overrides.append(override.replace(sorted_overrides[0]))
                sorted_overrides = sorted_overrides[1:]
            elif new_index < existing_index:
                merged_overrides.append(sorted_overrides[0])
                merged_overrides.append(override)
                sorted_overrides = sorted_overrides[1:]
            else:
                merged_overrides.append(override)
        else:
            merged_overrides.append(override)
    if len(sorted_overrides) > 0:
        merged_overrides.extend(sorted_overrides)
    return merged_overrides


class Devices(APIHandler[Device]):
    """Represents network devices."""

    obj_id_key = "mac"
    item_cls = Device
    process_messages = (MessageKey.DEVICE,)
    list_endpoint = ApiEndpoint(path="/stat/device")
    update_endpoint = ApiEndpoint(path="/rest/device/{api_item._id}")

    async def power_cycle_port(self, device: Device, port_idx: int) -> ApiResponse:
        """Power cycle a POE port."""
        return await self.send_cmd(device, "power-cycle", port_idx=port_idx)

    async def restart(self, device: Device, soft: bool = True):
        """Restart a network device."""
        return await self.send_cmd(
            device, "restart", reboot_type="soft" if soft else "hard"
        )

    async def send_cmd(self, device: Device, cmd: str, **kwargs) -> ApiResponse:
        """Upgrade network device."""
        return await self.client.post(
            ApiEndpoint(
                path="/cmd/devmgr",
            ),
            device,
            data={"cmd": cmd, "mac": device.mac, **kwargs},
        )

    async def set_led_status(
        self,
        device: Device,
        status: str = "on",
        brightness: int | None = None,
        color: str | None = None,
    ):
        """Set LED status of device."""
        updated_fields = {"led_override"}
        device.led_override = status
        if device.supports_led_ring:
            # Validate brightness parameter
            if brightness is not None:
                if 0 <= brightness <= 100:
                    device.led_override_color_brightness = brightness
                    updated_fields.add("led_override_color_brightness")
                else:
                    raise ValueError("Brightness must be within the range [0, 100].")

            # Validate color parameter
            if color is not None:
                if re.match(r"^#(?:[0-9a-fA-F]{3}){1,2}$", color):
                    device.led_override_color = color
                    updated_fields.add("led_override_color")
                else:
                    raise ValueError(
                        "Color must be a valid hex color code (e.g., '#00FF00')."
                    )

        return await self.save(device, updated_fields)

    async def set_outlet_overrides(
        self, device: Device, *overrides: DeviceOutletOverrides
    ) -> ApiResponse:
        """Assign the outlet overrides to the device.

        Any existing overrides will be updated with the non-None values given in the override.
        """
        device.outlet_overrides = cast(
            list[DeviceOutletOverrides],
            _merge_overrides(device.outlet_overrides, overrides, "index"),
        )
        return await self.save(device, {"outlet_overrides"})

    async def set_port_overrides(
        self, device: Device, *overrides: DevicePortOverrides
    ) -> ApiResponse:
        """Assign the outlet overrides to the device.

        Any existing overrides will be updated with the non-None values given in the override.
        """
        device.port_overrides = cast(
            list[DevicePortOverrides],
            _merge_overrides(device.port_overrides, overrides, "port_idx"),
        )
        return await self.save(device, {"port_overrides"})

    async def upgrade(self, device: Device) -> ApiResponse:
        """Upgrade network device."""
        return await self.send_cmd(device, "upgrade")
