"""WLANs as part of a UniFi network."""

from dataclasses import dataclass
import io

import segno.helpers

from .api import ApiItem, json_field


@dataclass
class Wlan(ApiItem):
    """Wlan type definition."""

    id: str = json_field("_id")

    bc_filter_enabled: bool | None = None
    bc_filter_list: list[str] | None = None
    dtim_mode: str | None = None
    dtim_na: int | None = None
    dtim_ng: int | None = None
    enabled: bool | None = None
    group_rekey: int | None = None
    is_guest: bool | None = None
    mac_filter_enabled: bool | None = None
    mac_filter_list: list[str] | None = None
    mac_filter_policy: str | None = None
    minrate_na_advertising_rates: bool | None = None
    minrate_na_beacon_rate_kbps: int | None = None
    minrate_na_data_rate_kbps: int | None = None
    minrate_na_enabled: bool | None = None
    minrate_na_mgmt_rate_kbps: int | None = None
    minrate_ng_advertising_rates: bool | None = None
    minrate_ng_beacon_rate_kbps: int | None = None
    minrate_ng_cck_rates_enabled: bool | None = None
    minrate_ng_data_rate_kbps: int | None = None
    minrate_ng_enabled: bool | None = None
    minrate_ng_mgmt_rate_kbps: int | None = None
    name: str | None = None
    name_combine_enabled: bool | None = None
    name_combine_suffix: str | None = None
    no2ghz_oui: bool | None = None
    schedule: list[str] | None = None
    security: str | None = None
    site_id: str | None = None
    usergroup_id: str | None = None
    wep_idx: int | None = None
    wlangroup_id: str | None = None
    wpa_enc: str | None = None
    wpa_mode: str | None = None
    x_iapp_key: str | None = None
    x_passphrase: str | None = None

    def generate_qr_code(self, kind: str = "png", scale: int = 4):
        """Generate a QR code for this WLAN."""
        buffer = io.BytesIO()
        qr_code = segno.helpers.make_wifi(
            ssid=self.name or "", password=self.x_passphrase, security=self.wpa_mode
        )
        qr_code.save(out=buffer, kind=kind, scale=scale)
        return buffer.getvalue()
