"""Event messages on state changes."""

from __future__ import annotations

from dataclasses import dataclass
import enum
import logging

from .api import ApiItem

LOGGER = logging.getLogger(__name__)


class EventKey(enum.Enum):
    """Key as part of event data object.

    "data": [{"key": "EVT_LU_Disconnected"}].
    """

    CONTROLLER_UPDATE_AVAILABLE = "EVT_AD_Update_Available"

    ACCESS_POINT_ADOPTED = "EVT_AP_Adopted"
    ACCESS_POINT_AUTO_READOPTED = "EVT_AP_AutoReadopted"
    ACCESS_POINT_CHANNEL_CHANGED = "EVT_AP_ChannelChanged"
    ACCESS_POINT_CONFIGURED = "EVT_AP_Configured"
    ACCESS_POINT_CONNECTED = "EVT_AP_Connected"
    ACCESS_POINT_DELETED = "EVT_AP_Deleted"
    ACCESS_POINT_DETECT_ROGUE_AP = "EVT_AP_DetectRogueAP"
    ACCESS_POINT_DISCOVERED_PENDING = "EVT_AP_DiscoveredPending"
    ACCESS_POINT_ISOLATED = "EVT_AP_Isolated"
    ACCESS_POINT_LOST_CONTACT = "EVT_AP_Lost_Contact"
    ACCESS_POINT_POSSIBLE_INTERFERENCE = "EVT_AP_PossibleInterference"
    ACCESS_POINT_RADAR_DETECTED = "EVT_AP_RadarDetected"
    ACCESS_POINT_RESTARTED = "EVT_AP_Restarted"
    ACCESS_POINT_RESTARTED_UNKNOWN = "EVT_AP_RestartedUnknown"
    ACCESS_POINT_UPGRADE_SCHEDULED = "EVT_AP_UpgradeScheduled"
    ACCESS_POINT_UPGRADE_FAILED = "EVT_AP_UpgradeFailed"
    ACCESS_POINT_UPGRADED = "EVT_AP_Upgraded"

    DREAM_MACHINE_CONNECTED = "EVT_DM_Connected"
    DREAM_MACHINE_LOST_CONTACT = "EVT_DM_Lost_Contact"
    DREAM_MACHINE_UPGRADED = "EVT_DM_Upgraded"

    GATEWAY_ADOPTED = "EVT_GW_Adopted"
    GATEWAY_AUTO_READOPTED = "EVT_GW_AutoReadopted"
    GATEWAY_CONFIGURED = "EVT_GW_Configured"
    GATEWAY_CONNECTED = "EVT_GW_Connected"
    GATEWAY_DELETED = "EVT_GW_Deleted"
    GATEWAY_LOST_CONTACT = "EVT_GW_Lost_Contact"
    GATEWAY_RESTARTED = "EVT_GW_Restarted"
    GATEWAY_RESTARTED_UNKNOWN = "EVT_GW_RestartedUnknown"
    GATEWAY_UPGRADED = "EVT_GW_Upgraded"
    GATEWAY_WAN_TRANSITION = "EVT_GW_WANTransition"

    SWITCH_ADOPTED = "EVT_SW_Adopted"
    SWITCH_AUTO_READOPTED = "EVT_SW_AutoReadopted"
    SWITCH_CONFIGURED = "EVT_SW_Configured"
    SWITCH_CONNECTED = "EVT_SW_Connected"
    SWITCH_DELETED = "EVT_SW_Deleted"
    SWITCH_DETECT_ROGUE_DHCP = "EVT_SW_DetectRogueDHCP"
    SWITCH_DISCOVERED_PENDING = "EVT_SW_DiscoveredPending"
    SWITCH_LOST_CONTACT = "EVT_SW_Lost_Contact"
    SWITCH_OVERHEAT = "EVT_SW_Overheat"
    SWITCH_POE_OVERLOAD = "EVT_SW_PoeOverload"
    SWITCH_POE_DISCONNECT = "EVT_SW_PoeDisconnect"
    SWITCH_RESTARTED = "EVT_SW_Restarted"
    SWITCH_RESTARTED_UNKNOWN = "EVT_SW_RestartedUnknown"
    SWITCH_STP_PORT_BLOCKING = "EVT_SW_StpPortBlocking"
    SWITCH_UPGRADE_SCHEDULED = "EVT_SW_UpgradeScheduled"
    SWITCH_UPGRADED = "EVT_SW_Upgraded"

    VOUCHER_CREATED = "EVT_AD_VoucherCreated"
    VOUCHER_DELETED = "EVT_AD_VoucherDeleted"

    WIRED_CLIENT_CONNECTED = "EVT_LU_Connected"
    WIRED_CLIENT_DISCONNECTED = "EVT_LU_Disconnected"
    WIRED_CLIENT_BLOCKED = "EVT_LC_Blocked"
    WIRED_CLIENT_UNBLOCKED = "EVT_LC_Unblocked"
    WIRELESS_CLIENT_CONNECTED = "EVT_WU_Connected"
    WIRELESS_CLIENT_DISCONNECTED = "EVT_WU_Disconnected"
    WIRELESS_CLIENT_BLOCKED = "EVT_WC_Blocked"
    WIRELESS_CLIENT_UNBLOCKED = "EVT_WC_Unblocked"
    WIRELESS_CLIENT_ROAM = "EVT_WU_Roam"
    WIRELESS_CLIENT_ROAM_RADIO = "EVT_WU_RoamRadio"

    WIRED_GUEST_CONNECTED = "EVT_LG_Connected"
    WIRED_GUEST_DISCONNECTED = "EVT_LG_Disconnected"
    WIRELESS_GUEST_AUTHENTICATION_ENDED = "EVT_WG_AuthorizationEnded"
    WIRELESS_GUEST_CONNECTED = "EVT_WG_Connected"
    WIRELESS_GUEST_DISCONNECTED = "EVT_WG_Disconnected"
    WIRELESS_GUEST_ROAM = "EVT_WG_Roam"
    WIRELESS_GUEST_ROAM_RADIO = "EVT_WG_RoamRadio"

    XG_AUTO_READOPTED = "EVT_XG_AutoReadopted"
    XG_CONNECTED = "EVT_XG_Connected"
    XG_LOST_CONTACT = "EVT_XG_Lost_Contact"
    XG_OUTLET_POWER_CYCLE = "EVT_XG_OutletPowerCycle"

    IPS_ALERT = "EVT_IPS_IpsAlert"

    AD_GUEST_UNAUTHORIZED = "EVT_AD_GuestUnauthorized"
    AD_LOGIN = "EVT_AD_Login"
    AD_SCHEDULE_UPGRADE_FAILED_NOT_FOUND = "EVT_AD_ScheduleUpgradeFailedNotFound"

    HOT_SPOT_AUTHED_BY_NO_AUTH = "EVT_HS_AuthedByNoAuth"
    HOT_SPOT_AUTHED_BY_PASSWORD = "EVT_HS_AuthedByPassword"
    HOT_SPOT_VOUCHER_USED = "EVT_HS_VoucherUsed"

    UNKNOWN = "unknown"

    @classmethod
    def _missing_(cls, value: object) -> EventKey:
        """Set default enum member if an unknown value is provided."""
        LOGGER.warning("Unsupported event key %s", value)
        return EventKey.UNKNOWN


@dataclass
class Event(ApiItem):
    """Event type definition."""

    _id: str | None = None
    ap: str = ""
    bytes: int = 0
    channel: int = 0
    client: str | None = None
    datetime: str | None = None
    duration: int = 0
    guest: str | None = None
    gw: str | None = None
    hostname: str = ""
    key: EventKey | None = None
    msg: str | None = None
    network: str | None = None
    radio: str = ""
    site_id: str = ""
    ssid: str = ""
    sw: str | None = None
    sw_name: str | None = None
    subsystem: str = ""
    time: int | None = None
    user: str | None = None
    version_from: str = ""
    version_to: str = ""

    @property
    def client_mac(self) -> str:
        """MAC address of client."""
        return self.user or self.client or self.guest or ""

    @property
    def device(self) -> str:
        """MAC address of device."""
        return self.ap or self.gw or self.sw or ""

    @property
    def event(self) -> str | None:
        """Event key e.g. 'EVT_WU_Disconnected'.

        To be removed.
        """
        return self.key.value if self.key else None

    @property
    def mac(self) -> str:
        """MAC of client or device."""
        if self.client_mac:
            return self.client_mac
        if self.device:
            return self.device
        return ""
