"""API management class and base class for the different end points."""

from __future__ import annotations

from abc import ABC
from collections import UserDict, defaultdict
from collections.abc import Callable
import enum
from typing import TYPE_CHECKING, Any, final

from ..models.api import ApiItem, ApiRequest

if TYPE_CHECKING:
    from ..controller import Controller
    from ..models.message import Message, MessageKey


class ItemEvent(enum.Enum):
    """The event action of the item."""

    ADDED = "added"
    CHANGED = "changed"
    DELETED = "deleted"


CallbackType = Callable[[ItemEvent, str], None]
SubscriptionType = tuple[CallbackType, tuple[ItemEvent, ...] | None]
UnsubscribeType = Callable[[], None]

ID_FILTER_ALL = "*"


class SubscriptionHandler(ABC):
    """Manage subscription and notification to subscribers."""

    def __init__(self) -> None:
        """Initialize subscription handler."""
        super().__init__()
        self._subscribers: dict[str, list[SubscriptionType]] = defaultdict(list)

    def signal_subscribers(self, event: ItemEvent, obj_id: str) -> None:
        """Signal subscribers."""
        subscribers: list[SubscriptionType] = (
            self._subscribers[obj_id] + self._subscribers[ID_FILTER_ALL]
        )
        for callback, event_filter in subscribers:
            if event_filter is not None and event not in event_filter:
                continue
            callback(event, obj_id)

    def subscribe(
        self,
        callback: CallbackType,
        event_filter: tuple[ItemEvent, ...] | ItemEvent | None = None,
        id_filter: tuple[str] | str | None = None,
    ) -> UnsubscribeType:
        """Subscribe to added events."""
        if isinstance(event_filter, ItemEvent):
            event_filter = (event_filter,)
        subscription = (callback, event_filter)

        _id_filter: tuple[str]
        if id_filter is None:
            _id_filter = (ID_FILTER_ALL,)
        elif isinstance(id_filter, str):
            _id_filter = (id_filter,)

        for obj_id in _id_filter:
            self._subscribers[obj_id].append(subscription)

        def unsubscribe() -> None:
            for obj_id in _id_filter:
                if subscription not in self._subscribers[obj_id]:
                    continue
                self._subscribers[obj_id].remove(subscription)

        return unsubscribe


class APIHandler[T: ApiItem](SubscriptionHandler, UserDict[T]):
    """Base class for a map of API Items."""

    obj_id_key: str
    item_cls: type[T]
    api_request: ApiRequest
    process_messages: tuple[MessageKey, ...] = ()
    remove_messages: tuple[MessageKey, ...] = ()

    def __init__(self, controller: Controller) -> None:
        """Initialize API handler."""
        super().__init__()
        self.controller = controller

        if message_filter := self.process_messages + self.remove_messages:
            controller.messages.subscribe(self.process_message, message_filter)

    @final
    async def update(self) -> None:
        """Refresh data."""
        raw = await self.controller.request(self.api_request)
        self.process_raw(raw.data)

    @final
    def process_raw(self, raw: list[dict[str, Any]]) -> None:
        """Process full raw response."""
        for raw_item in raw:
            self.process_item(raw_item)

    @final
    def process_message(self, message: Message) -> None:
        """Process and forward websocket data."""
        if message.meta.message in self.process_messages:
            self.process_item(message.data)

        elif message.meta.message in self.remove_messages:
            self.remove_item(message.data)

    @final
    def process_item(self, raw: dict[str, Any]) -> None:
        """Process item data."""
        if self.obj_id_key not in raw:
            return

        obj_id: str
        obj_is_known = (obj_id := raw[self.obj_id_key]) in self
        self[obj_id] = self.item_cls.from_json(data=raw)

        self.signal_subscribers(
            ItemEvent.CHANGED if obj_is_known else ItemEvent.ADDED,
            obj_id,
        )

    @final
    def remove_item(self, raw: dict[str, Any]) -> None:
        """Remove item."""
        self.pop(raw[self.obj_id_key])

    def pop(self, obj_id: str):
        """If obj_id is in the dictionary, remove it and signal subscribers."""
        item = super().pop(obj_id, None)
        if item:
            self.signal_subscribers(ItemEvent.DELETED, obj_id)
