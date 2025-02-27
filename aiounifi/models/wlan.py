"""WLANs as part of a UniFi network."""

from dataclasses import dataclass
import io

import segno.helpers

from .api import ApiItem, ApiRequest, json_field


@dataclass
class Wlan(ApiItem):
    """Wlan type definition."""

    dtim_mode: str
    dtim_na: int
    dtim_ng: int
    enabled: bool
    group_rekey: int
    minrate_na_advertising_rates: bool
    minrate_na_data_rate_kbps: int
    minrate_ng_advertising_rates: bool
    minrate_ng_data_rate_kbps: int
    name: str
    schedule: list[str]
    security: str
    site_id: str
    usergroup_id: str
    wpa_enc: str
    wpa_mode: str
    x_iapp_key: str

    id: str = json_field("_id")
    is_guest: bool | None = None
    bc_filter_enabled: bool | None = None
    bc_filter_list: list[str] | None = None
    mac_filter_enabled: bool | None = None
    mac_filter_list: list[str] | None = None
    mac_filter_policy: str | None = None
    minrate_na_beacon_rate_kbps: int | None = None
    minrate_na_enabled: bool | None = None
    minrate_na_mgmt_rate_kbps: int | None = None
    minrate_ng_beacon_rate_kbps: int | None = None
    minrate_ng_cck_rates_enabled: bool | None = None
    minrate_ng_enabled: bool | None = None
    minrate_ng_mgmt_rate_kbps: int | None = None
    name_combine_enabled: bool | None = None
    name_combine_suffix: str | None = None
    no2ghz_oui: bool | None = None
    wep_idx: int | None = None
    wlangroup_id: str | None = None
    x_passphrase: str | None = None


@dataclass
class WlanListRequest(ApiRequest):
    """Request object for wlan list."""

    def __init__(self):
        """Create wlan list request."""
        super().__init__(method="get", path="/rest/wlanconf")


@dataclass
class WlanChangePasswordRequest(ApiRequest):
    """Request object for wlan password change."""

    def __init__(self, wlan_id: str, password: str):
        """Create wlan password change request."""
        super().__init__(
            method="put",
            path=f"/rest/wlanconf/{wlan_id}",
            data={"x_passphrase": password},
        )


@dataclass
class WlanEnableRequest(ApiRequest):
    """Request object for wlan enable."""

    def __init__(self, wlan_id: str, enable: bool):
        """Create wlan enable request."""
        super().__init__(
            method="put",
            path=f"/rest/wlanconf/{wlan_id}",
            data={"enabled": enable},
        )


def wlan_qr_code(
    name: str, password: str | None, kind: str = "png", scale: int = 4
) -> bytes:
    """Generate WLAN QR code."""
    buffer = io.BytesIO()
    qr_code = segno.helpers.make_wifi(ssid=name, password=password, security="WPA")
    qr_code.save(out=buffer, kind=kind, scale=scale)
    return buffer.getvalue()
