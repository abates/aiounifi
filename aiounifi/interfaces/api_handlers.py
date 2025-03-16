"""API management class and base class for the different end points."""

from __future__ import annotations

from abc import ABC
from collections import UserDict, defaultdict
from dataclasses import dataclass
import enum
from typing import TYPE_CHECKING, Any, Protocol, final

from ..models.api import ApiEndpoint, ApiItem, ApiResponse

if TYPE_CHECKING:
    from ..client import UnifiClient
    from ..models.message import Message, MessageKey


class ItemEvent(enum.Enum):
    """The event action of the item."""

    ADDED = "added"
    CHANGED = "changed"
    DELETED = "deleted"


ID_FILTER_ALL = "*"


class Callback(Protocol):
    """An event callback."""

    def __call__(self, event: ItemEvent, obj_id: str) -> None: ...  # noqa: D102


class Unsubscribe(Protocol):
    """Remove a event callback from the subscription handler."""

    def __call__(self) -> None: ...  # type: ignore # noqa: D102


@dataclass
class Subscription:
    """A subscription for a message stream."""

    callback: Callback
    event_filter: set[ItemEvent] | None


class SubscriptionHandler(ABC):
    """Manage subscription and notification to subscribers."""

    def __init__(self) -> None:
        """Initialize subscription handler."""
        super().__init__()
        self._subscribers: dict[str, list[Subscription]] = defaultdict(list)

    def signal_subscribers(self, event: ItemEvent, obj_id: str) -> None:
        """Signal subscribers."""
        subscribers: list[Subscription] = (
            self._subscribers[obj_id] + self._subscribers[ID_FILTER_ALL]
        )
        for subscriber in subscribers:
            if subscriber.event_filter is None or event in subscriber.event_filter:
                subscriber.callback(
                    event,
                    obj_id,
                )

    def subscribe(
        self,
        callback: Callback,
        event_filter: tuple[ItemEvent, ...] | ItemEvent | None = None,
        id_filter: tuple[str] | str | None = None,
    ) -> Unsubscribe:
        """Subscribe to added events."""
        if isinstance(event_filter, ItemEvent):
            event_filter = (event_filter,)

        subscription = Subscription(
            callback=callback,
            event_filter=None if event_filter is None else set(event_filter),
        )

        if id_filter is None:
            id_filter = (ID_FILTER_ALL,)
        elif isinstance(id_filter, str):
            id_filter = (id_filter,)

        for obj_id in id_filter:
            self._subscribers[obj_id].append(subscription)

        def unsubscribe() -> None:
            for obj_id in id_filter:
                if subscription not in self._subscribers[obj_id]:
                    continue
                self._subscribers[obj_id].remove(subscription)
                if not self._subscribers[obj_id]:
                    del self._subscribers[obj_id]

        return unsubscribe  # type: ignore


class APIHandler[T: ApiItem](SubscriptionHandler, UserDict[str, T]):
    """Base class for a map of API Items."""

    obj_id_key: str
    item_cls: type[T]

    process_messages: tuple[MessageKey, ...] = ()
    remove_messages: tuple[MessageKey, ...] = ()

    list_endpoint: ApiEndpoint | None = None
    create_endpoint: ApiEndpoint | None = None
    update_endpoint: ApiEndpoint | None = None
    delete_endpoint: ApiEndpoint | None = None

    def __init__(self, client: UnifiClient) -> None:
        """Initialize API handler."""
        super().__init__()
        self.client = client

        if message_filter := self.process_messages + self.remove_messages:
            client.messages.subscribe(self.process_message, message_filter)

    @final
    async def update(self) -> None:  # type: ignore
        """Refresh data."""
        if self.list_endpoint is None:
            raise NotImplementedError(
                f"{self.__class__.__name__} does not implement a list endpoint."
            )

        response = await self.client.get(self.list_endpoint)
        if response:
            self.process_raw(response.data)

    async def save(self, api_item: T, fields: set[str] | None = None) -> ApiResponse:
        """Save a previously created api item."""
        if self.update_endpoint is None:
            raise NotImplementedError(
                f"{self.__class__.__name__} does not implement an update endpoint."
            )

        data = api_item.to_json(fields)
        response = await self.client.put(self.update_endpoint, api_item, data)
        if response:
            self.process_raw(response.data)
        return response

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
            self.pop(message.data[self.obj_id_key], None)

    def process_item(self, raw: dict[str, Any]) -> None:
        """Process item data."""
        if self.obj_id_key not in raw:
            return

        self[raw[self.obj_id_key]] = self.item_cls.from_json(data=raw)

    def __setitem__(self, key, item):
        """Set the handler's collection key to item."""
        changed = key in self
        super().__setitem__(key, item)
        self.signal_subscribers(
            ItemEvent.CHANGED if changed else ItemEvent.ADDED,
            key,
        )

    def __delitem__(self, obj_id: str):
        """If obj_id is in the dictionary, remove it and signal subscribers."""
        item = self.get(obj_id)
        if item is not None:
            super().__delitem__(obj_id)
            self.signal_subscribers(ItemEvent.DELETED, obj_id)
