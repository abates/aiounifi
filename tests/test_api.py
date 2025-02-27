"""Test API handlers."""

from collections import defaultdict
from unittest.mock import Mock

import pytest

from aiounifi.interfaces.api_handlers import (
    ID_FILTER_ALL,
    APIHandler,
    ItemEvent,
    SubscriptionHandler,
)
from aiounifi.models.api import ApiResponse
from aiounifi.models.message import Message, MessageKey, Meta


@pytest.mark.parametrize(
    ("event_filter", "id_filter", "subscribers"),
    [
        (None, None, {"*": None}),
        (ItemEvent.ADDED, "1234", {"1234": (ItemEvent.ADDED,)}),
        (ItemEvent.CHANGED, "1234", {"1234": (ItemEvent.CHANGED,)}),
        (ItemEvent.DELETED, "1234", {"1234": (ItemEvent.DELETED,)}),
        (
            ItemEvent.DELETED,
            ("1234", "5678"),
            {"1234": (ItemEvent.DELETED,), "5678": (ItemEvent.DELETED,)},
        ),
        (
            (ItemEvent.ADDED, ItemEvent.DELETED),
            ("1234", "5678"),
            {
                "1234": (
                    ItemEvent.ADDED,
                    ItemEvent.DELETED,
                ),
                "5678": (
                    ItemEvent.ADDED,
                    ItemEvent.DELETED,
                ),
            },
        ),
    ],
)
def test_subscription_handler_subscribe(event_filter, id_filter, subscribers):
    """Test that subscriptions are setup correctly."""

    class TestHandler(SubscriptionHandler):
        pass

    handler = TestHandler()

    unsub = handler.subscribe(callback := Mock(), event_filter, id_filter)
    assert handler._subscribers.keys() == subscribers.keys()
    for key in subscribers:
        assert handler._subscribers[key][0].event_filter == subscribers[key]
        assert handler._subscribers[key][0].callback is callback

    unsub()
    assert len(handler._subscribers) == 0


@pytest.mark.parametrize(
    ("event_filter", "id_filter", "events", "signaled_events"),
    [
        (
            ItemEvent.ADDED,
            "1234",
            [(ItemEvent.ADDED, "1234")],
            {ItemEvent.ADDED: ["1234"]},
        ),
        (
            ItemEvent.ADDED,
            "1234",
            [(ItemEvent.ADDED, "1234"), (ItemEvent.ADDED, "5678")],
            {ItemEvent.ADDED: ["1234"]},
        ),
        (
            ItemEvent.ADDED,
            ("1234", "5678"),
            [(ItemEvent.ADDED, "1234"), (ItemEvent.ADDED, "5678")],
            {ItemEvent.ADDED: ["1234", "5678"]},
        ),
        (
            ItemEvent.ADDED,
            ("1234", "5678"),
            [(ItemEvent.ADDED, "1234"), (ItemEvent.DELETED, "5678")],
            {ItemEvent.ADDED: ["1234"]},
        ),
        (
            None,
            ("1234", "5678"),
            [(ItemEvent.ADDED, "1234"), (ItemEvent.DELETED, "5678")],
            {ItemEvent.ADDED: ["1234"], ItemEvent.DELETED: ["5678"]},
        ),
        (
            ItemEvent.ADDED,
            ID_FILTER_ALL,
            [(ItemEvent.ADDED, "1234"), (ItemEvent.ADDED, "5678")],
            {ItemEvent.ADDED: ["1234", "5678"]},
        ),
    ],
)
def test_subscription_handler_signal(event_filter, id_filter, events, signaled_events):
    """Verify that signaled events are dispatched correctly."""

    class TestHandler(SubscriptionHandler):
        pass

    handler = TestHandler()

    class Callback:
        def __init__(self):
            self.events = defaultdict(list)

        def __call__(self, event, obj_id):
            self.events[event].append(obj_id)

    callback = Callback()
    handler.subscribe(callback, event_filter, id_filter)
    for event, obj_id in events:
        handler.signal_subscribers(event, obj_id)
    assert callback.events == signaled_events


@pytest.mark.parametrize(
    ("process_filter", "remove_filter", "expected"),
    [
        ((), (), ()),
        ((MessageKey.CLIENT,), (), (MessageKey.CLIENT,)),
        (
            (MessageKey.CLIENT, MessageKey.DEVICE),
            (),
            (MessageKey.CLIENT, MessageKey.DEVICE),
        ),
        (
            (MessageKey.CLIENT, MessageKey.DEVICE),
            (MessageKey.CLIENT_REMOVED,),
            (MessageKey.CLIENT, MessageKey.DEVICE, MessageKey.CLIENT_REMOVED),
        ),
    ],
)
def test_api_handler_init(process_filter, remove_filter, expected):
    """Verify message process subscriptions take place."""
    controller = Mock()
    subscribe = Mock()
    controller.messages.subscribe = subscribe

    class TestHandler(APIHandler):
        process_messages = process_filter
        remove_messages = remove_filter

    handler = TestHandler(controller)
    if expected:
        subscribe.assert_called()
        subscribe.assert_called_with(handler.process_message, expected)
    else:
        subscribe.assert_not_called()


def test_api_handler_signaling():
    """Verify that signals are sent for items being added/updated/removed from a handler."""
    handler = APIHandler(None)
    callback = Mock()
    handler.subscribe(callback, None, "*")
    handler[0] = 0
    callback.assert_called_with(ItemEvent.ADDED, 0)
    callback.reset_mock()

    handler[0] = 1
    callback.assert_called_with(ItemEvent.CHANGED, 0)
    callback.reset_mock()

    handler.pop(0)
    callback.assert_called_with(ItemEvent.DELETED, 0)
    callback.reset_mock()

    handler.pop(0, None)
    callback.assert_not_called()
    callback.reset_mock()

    handler[0] = 0
    callback.assert_called_with(ItemEvent.ADDED, 0)
    callback.reset_mock()

    del handler[0]
    callback.assert_called_with(ItemEvent.DELETED, 0)


@pytest.mark.parametrize(
    ("response", "expected"),
    [
        ([{"id": 1, "name": "data1"}], {1: {"id": 1, "name": "data1"}}),
        (
            [{"id": 1, "name": "data1"}, {"id": 2, "name": "data2"}],
            {1: {"id": 1, "name": "data1"}, 2: {"id": 2, "name": "data2"}},
        ),
        (
            [
                {"id": 1, "name": "data1"},
                {"id": 2, "name": "data2"},
                {"_id": 3, "name": "data3"},
            ],
            {1: {"id": 1, "name": "data1"}, 2: {"id": 2, "name": "data2"}},
        ),
    ],
)
async def test_api_handler_update(response, expected):
    """Verify the behavior of the update method and its related helpers."""

    controller = Mock()
    api_request_str = "API_REQUEST"

    async def request(request_obj):
        if request_obj is not api_request_str:
            raise ValueError("Didn't get expected request object")
        return ApiResponse(meta={}, data=response)

    controller.request = request

    item_class = Mock()
    item_class.from_json = lambda data: data

    class TestHandler(APIHandler):
        obj_id_key = "id"
        item_cls = item_class
        api_request = api_request_str

    handler = TestHandler(controller)
    await handler.update()
    assert handler.data == expected


@pytest.mark.parametrize(
    ("messages", "expected"),
    [
        (
            [(MessageKey.CLIENT, {"id": 1, "name": "client1"})],
            {1: {"id": 1, "name": "client1"}},
        ),
        (
            [
                (MessageKey.CLIENT, {"id": 1, "name": "client1"}),
                (MessageKey.CLIENT, {"id": 2, "name": "client2"}),
            ],
            {1: {"id": 1, "name": "client1"}, 2: {"id": 2, "name": "client2"}},
        ),
        (
            [
                (MessageKey.CLIENT, {"id": 1, "name": "client1"}),
                (MessageKey.CLIENT, {"id": 2, "name": "client2"}),
                (MessageKey.CLIENT_REMOVED, {"id": 2, "name": "client2"}),
            ],
            {1: {"id": 1, "name": "client1"}},
        ),
    ],
)
def test_api_handler_process_message(messages, expected):
    """Verify message processing behavior."""
    item_class = Mock()
    item_class.from_json = lambda data: data

    class TestHandler(APIHandler):
        obj_id_key = "id"
        item_cls = item_class
        process_messages = (MessageKey.CLIENT,)
        remove_messages = (MessageKey.CLIENT_REMOVED,)

    handler = TestHandler(Mock())
    for message_key, message in messages:
        handler.process_message(
            Message(meta=Meta.from_dict({"message": message_key}), data=message)
        )

    assert handler.data == expected
