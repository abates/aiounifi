"""WLANs as part of a UniFi network."""

from dataclasses import dataclass
import io
from typing import Self

import segno.helpers

from .api import ApiItem, ApiRequest, json_field


@dataclass
class Wlan(ApiItem):
    """Wlan type definition."""

    id: str = json_field("_id")
    bc_filter_enabled: bool
    bc_filter_list: list[str]
    dtim_mode: str
    dtim_na: int
    dtim_ng: int
    enabled: bool
    group_rekey: int
    mac_filter_list: list[str]
    mac_filter_policy: str
    minrate_na_advertising_rates: bool
    minrate_na_beacon_rate_kbps: int
    minrate_na_data_rate_kbps: int
    minrate_na_mgmt_rate_kbps: int
    minrate_ng_advertising_rates: bool
    minrate_ng_beacon_rate_kbps: int
    minrate_ng_data_rate_kbps: int
    minrate_ng_mgmt_rate_kbps: int
    name: str
    schedule: list[str]
    security: str
    site_id: str
    usergroup_id: str
    wep_idx: int
    wlangroup_id: str
    wpa_enc: str
    wpa_mode: str
    x_iapp_key: str

    is_guest: bool | None = None
    mac_filter_enabled: bool | None = None
    minrate_na_enabled: bool | None = None
    minrate_ng_cck_rates_enabled: bool | None = None
    minrate_ng_enabled: bool | None = None
    name_combine_enabled: bool | None = None
    name_combine_suffix: str | None = None
    no2ghz_oui: bool | None = None
    x_passphrase: str | None = None


@dataclass
class WlanListRequest(ApiRequest):
    """Request object for wlan list."""

    @classmethod
    def create(cls) -> Self:
        """Create wlan list request."""
        return cls(method="get", path="/rest/wlanconf")


@dataclass
class WlanChangePasswordRequest(ApiRequest):
    """Request object for wlan password change."""

    @classmethod
    def create(cls, wlan_id: str, password: str) -> Self:
        """Create wlan password change request."""
        return cls(
            method="put",
            path=f"/rest/wlanconf/{wlan_id}",
            data={"x_passphrase": password},
        )


@dataclass
class WlanEnableRequest(ApiRequest):
    """Request object for wlan enable."""

    @classmethod
    def create(cls, wlan_id: str, enable: bool) -> Self:
        """Create wlan enable request."""
        return cls(
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
