"""UniFi system information model."""

from __future__ import annotations

from dataclasses import dataclass, field

from .api import ApiItem, ApiRequest, json_field


@dataclass
class SystemInformation(ApiItem):
    """System information type definition."""

    anonymous_controller_id: str | None = None
    autobackup: bool | None = None
    build: str | None = None
    console_display_version: str | None = None
    data_retention_days: int | None = None
    data_retention_time_in_hours_for_5minutes_scale: int | None = None
    data_retention_time_in_hours_for_daily_scale: int | None = None
    data_retention_time_in_hours_for_hourly_scale: int | None = None
    data_retention_time_in_hours_for_monthly_scale: int | None = None
    data_retention_time_in_hours_for_others: int | None = None
    debug_device: str | None = None
    debug_mgmt: str | None = None
    debug_sdn: str | None = None
    debug_setting_preference: str | None = None
    debug_system: str | None = None
    default_site_device_auth_password_alert: bool | None = None
    device_type: str | None = json_field("ubnt_device_type", default=None)
    facebook_wifi_registered: bool | None = None
    has_webrtc_support: bool | None = None
    hostname: str | None = None
    https_port: int | None = None
    image_maps_use_google_engine: bool | None = None
    inform_port: int | None = None
    ip_address: list[str] = json_field("ip_addrs", default_factory=list)
    is_cloud_console: bool | None = None
    live_chat: str | None = None
    name: str | None = None
    override_inform_host: bool | None = None
    portal_http_port: int | None = None
    previous_version: str | None = None
    radius_disconnect_running: bool | None = None
    sso_app_id: str | None = None
    sso_app_sec: str | None = None
    store_enabled: str | None = None
    timezone: str | None = None
    udm_version: str | None = None
    unifi_go_enabled: bool | None = None
    unsupported_device_count: int | None = None
    unsupported_device_list: list[str] = field(default_factory=list)
    update_available: bool | None = None
    update_downloaded: bool | None = None
    uptime: int | None = None
    version: str | None = None


@dataclass
class SystemInformationRequest(ApiRequest):
    """Request object for system information."""

    def __init__(self):
        """Create system information request."""
        super().__init__(method="get", path="/stat/sysinfo")
