"""Test events.

pytest --cov-report term-missing --cov=aiounifi.events tests/test_events.py
"""

from unittest.mock import Mock

import pytest

from aiounifi.interfaces.events import EventHandler
from aiounifi.models.event import Event, EventKey
from aiounifi.models.message import Message, MessageKey, Meta

EVENT_HANDLER_DATA = [
    (None, True),  # No filters
    (EventKey.SWITCH_LOST_CONTACT, True),  # Filter correct
    (EventKey.SWITCH_CONNECTED, False),  # Filter incorrect
]


@pytest.mark.parametrize(("event_filter", "expected"), EVENT_HANDLER_DATA)
def test_event_handler(event_filter, expected):
    """Verify event handler behaves according to configured filters."""
    event_handler = EventHandler(controller=Mock())

    filters = {}
    if event_filter:
        filters["event_filter"] = event_filter

    unsubscribe_callback = event_handler.subscribe(mock_callback := Mock(), **filters)
    assert len(event_handler) == 1
    assert unsubscribe_callback

    event_handler.handler(
        Message(
            meta=Meta("ok", MessageKey.EVENT, {}),
            data={
                "_id": "5eae7fe02ab79c00f9d38960",
                "datetime": "2020-05-03T08:25:04Z",
                "key": "EVT_SW_Lost_Contact",
                "msg": "Switch[00:..:00] was disconnected",
                "site_id": "default",
                "subsystem": "lan",
                "sw": "00:..:00",
                "sw_name": "switch name",
                "time": 1588494304030,
            },
        ),
    )
    assert mock_callback.called is expected

    unsubscribe_callback()
    assert len(event_handler) == 0


def test_unsupported_event_key():
    """Test empty event."""
    event = Event.from_json({"key": "unsupported"})
    assert event.key == EventKey.UNKNOWN


def test_empty_event():
    """Test empty event."""
    empty = Event.from_json({})

    assert empty.event is None
    assert empty.key is None
    assert empty.datetime is None
    assert empty.msg is None
    assert empty.time is None
    assert empty.mac == ""
    assert empty.ap == ""
    assert empty.bytes == 0
    assert empty.channel == 0
    assert empty.duration == 0
    assert empty.hostname == ""
    assert empty.radio == ""
    assert empty.subsystem == ""
    assert empty.site_id == ""
    assert empty.ssid == ""


@pytest.mark.parametrize(
    ("event", "expected"),
    [
        (Event(user="01aa:bbcc:ddee"), "01aa:bbcc:ddee"),
        (Event(user="01aa:bbcc:ddee", client="02aa:bbcc:ddee"), "01aa:bbcc:ddee"),
        (
            Event(
                user="01aa:bbcc:ddee", client="02aa:bbcc:ddee", guest="03aa:bbcc:ddee"
            ),
            "01aa:bbcc:ddee",
        ),
        (
            Event(
                user="01aa:bbcc:ddee",
                client="02aa:bbcc:ddee",
                guest="03aa:bbcc:ddee",
                ap="04aa:bbcc:ddee",
            ),
            "01aa:bbcc:ddee",
        ),
        (
            Event(
                user="01aa:bbcc:ddee",
                client="02aa:bbcc:ddee",
                guest="03aa:bbcc:ddee",
                ap="04aa:bbcc:ddee",
                gw="05aa:bbcc:ddee",
            ),
            "01aa:bbcc:ddee",
        ),
        (
            Event(
                user="01aa:bbcc:ddee",
                client="02aa:bbcc:ddee",
                guest="03aa:bbcc:ddee",
                ap="04aa:bbcc:ddee",
                gw="05aa:bbcc:ddee",
                sw="06aa:bbcc:ddee",
            ),
            "01aa:bbcc:ddee",
        ),
        (
            Event(
                client="02aa:bbcc:ddee",
                guest="03aa:bbcc:ddee",
                ap="04aa:bbcc:ddee",
                gw="05aa:bbcc:ddee",
                sw="06aa:bbcc:ddee",
            ),
            "02aa:bbcc:ddee",
        ),
        (
            Event(
                guest="03aa:bbcc:ddee",
                ap="04aa:bbcc:ddee",
                gw="05aa:bbcc:ddee",
                sw="06aa:bbcc:ddee",
            ),
            "03aa:bbcc:ddee",
        ),
        (
            Event(ap="04aa:bbcc:ddee", gw="05aa:bbcc:ddee", sw="06aa:bbcc:ddee"),
            "04aa:bbcc:ddee",
        ),
        (Event(gw="05aa:bbcc:ddee", sw="06aa:bbcc:ddee"), "05aa:bbcc:ddee"),
        (Event(sw="06aa:bbcc:ddee"), "06aa:bbcc:ddee"),
        (Event(), ""),
    ],
)
def test_event_mac(event: Event, expected: str):
    """Verify correct mac address is returned for `client_mac`."""
    assert event.mac == expected
