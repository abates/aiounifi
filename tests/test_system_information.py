"""Test system information API."""

# import pytest

# from aiounifi.client import UnifiClient

# from .fixtures import SYSTEM_INFORMATION


# @pytest.mark.parametrize("system_information_payload", [[SYSTEM_INFORMATION]])
# @pytest.mark.usefixtures("_mock_endpoints")
# async def test_system_information(unifi_controller: UnifiClient) -> None:
#     """Test port forwarding interface and model."""
#     system_information = unifi_controller.system_information
#     await system_information.update()
#     assert len(system_information.values()) == 1

#     sys_info = next(iter(system_information.values()))
#     assert sys_info.anonymous_controller_id == "24f81231-a456-4c32-abcd-f5612345385f"
#     assert sys_info.device_type == "UDMPRO"
#     assert sys_info.hostname == "UDMP"
#     assert sys_info.ip_address == ["1.2.3.4"]
#     assert sys_info.is_cloud_console is False
#     assert sys_info.name == "UDMP"
#     assert sys_info.previous_version == "7.4.156"
#     assert sys_info.update_available is False
#     assert sys_info.uptime == 1196290
#     assert sys_info.version == "7.4.162"
