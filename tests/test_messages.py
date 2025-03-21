"""Test messages.

pytest --cov-report term-missing --cov=aiounifi.messages tests/test_messages.py
"""

from unittest.mock import Mock, patch

import pytest

from aiounifi.interfaces.messages import MessageHandler
from aiounifi.models.message import Message, MessageKey

MESSAGE_HANDLER_DATA = [
    (None, False),  # No subscriber registered
    (MessageKey.CLIENT_REMOVED, True),  # Filter correct
    (MessageKey.CLIENT, False),  # Filter incorrect
    ((MessageKey.CLIENT, MessageKey.CLIENT_REMOVED), True),  # Filter correct
]


@pytest.mark.parametrize(("message_filter", "expected"), MESSAGE_HANDLER_DATA)
def test_message_handler(message_filter, expected):
    """Verify message handler behaves according to configured filters."""
    message_handler = MessageHandler(controller=Mock())

    filters = {}
    if message_filter:
        filters["message_filter"] = message_filter

    unsubscribe_callback = message_handler.subscribe(mock_callback := Mock(), **filters)
    assert len(message_handler) == 1
    assert unsubscribe_callback

    message_handler.handler(
        {
            "meta": {
                "rc": "ok",
                "message": MessageKey.CLIENT_REMOVED.value,
            },
            "data": [{}],
        }
    )
    assert mock_callback.called is expected

    unsubscribe_callback()
    assert len(message_handler) == 0


def test_unsupported_message_key():
    """Validate unsupported message key handling."""
    message = Message.from_dict(
        {
            "meta": {
                "rc": "ok",
                "message": "Unsupported",
            },
            "data": [{}],
        }
    )
    assert message.meta.message == MessageKey.UNKNOWN


@patch("aiounifi.interfaces.messages.LOGGER")
def test_message_handler_bad_json_data(logger_mock):
    """Verify message handler catches json error."""
    MessageHandler(controller=Mock()).new_data(b"")
    assert logger_mock.debug.called
