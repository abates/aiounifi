"""API management class and base class for the different end points."""

from abc import ABC
from collections.abc import Callable
import contextlib
from copy import deepcopy
from dataclasses import dataclass, field, fields
from types import UnionType
from typing import (
    Any,
    Protocol,
    TypeVar,
    get_args,
    get_origin,
    get_type_hints,
)


@dataclass
class BaseEndpoint:
    """Represents a basic REST endpoint."""

    path: str
    version: int = 1

    def format(self, *args: object, **kwargs: object) -> str:
        """Get the path of the endpoint."""

        path = f"/api{self.path}" if self.version == 1 else f"/api/v2{self.path}"
        return path.format(*args, **kwargs)


@dataclass
class ApiEndpoint(BaseEndpoint):
    """Encapsulates an API endpoint with its HTTP method and path template."""

    def __post_init__(self):
        """Update the path with site specific info."""
        if self.version == 1:
            self.path = f"/s/{{site}}{self.path}"
        else:
            self.path = f"/site/{{site}}{self.path}"


@dataclass
class ApiResponse:
    """Common response."""

    meta: dict[str, Any] = field(default_factory=dict)
    data: list[dict[str, Any]] = field(default_factory=list)


def _get_annotation(annotation):
    if isinstance(annotation, UnionType):
        args = get_args(annotation)
        if len(args) == 2:
            annotation = args[0]
            if annotation is None:
                annotation = args[1]
        else:
            raise ValueError(
                f"ApiItem type hints only support single type or optional single type. Got {len(args)} types"
            )
    return annotation, get_origin(annotation), get_args(annotation)


class FieldProcessor(Protocol):
    """Type definition for a field processor method."""

    def __call__(self, kwargs: dict[str, Any]) -> None: ...  # noqa: D102


ApiItem_T = TypeVar("ApiItem_T", bound="ApiItem")


@dataclass
class ApiItem(ABC):
    """Base class for all end points using APIItems class."""

    raw: dict[str, Any] = field(init=False, compare=False)

    @classmethod
    def _api_item_annotations(cls) -> dict[str, FieldProcessor]:
        """Lookup dataclass annotations and create processing methods that are used in from_json."""

        try:
            return getattr(cls, "__api_item_annotations")
        except AttributeError:
            api_item_annotations = {}
            setattr(cls, "__api_item_annotations", api_item_annotations)

        annotations = get_type_hints(cls)
        for api_field in fields(cls):  # type: ignore
            if api_field.name == "raw":
                continue

            custom_initializer = api_field.metadata.get("custom_initializer", None)
            annotation, origin, args = _get_annotation(annotations[api_field.name])
            api_item_annotations[api_field.name] = (  # type: ignore
                cls._generate_field_processor(
                    api_field.name,
                    annotation,
                    origin,
                    args,
                    custom_initializer=custom_initializer,
                )
            )

        return api_item_annotations

    @staticmethod
    def _generate_field_processor(
        field_name: str,
        annotation: type,
        origin: type,
        args: tuple[Any, ...],
        custom_initializer: Callable[[Any], Any] | None = None,
    ) -> FieldProcessor:
        if origin is list:
            child_cls = args[0]

            def process_api_item_list(kwargs: dict[str, Any]):
                children = kwargs[field_name]
                if isinstance(children, list):
                    kwargs[field_name] = []
                    for child in children:
                        if issubclass(child_cls, ApiItem):
                            kwargs[field_name].append(child_cls.from_json(child))
                        else:
                            kwargs[field_name].append(child_cls(child))
                else:
                    raise ValueError(
                        f"Expected {field_name} to be a list but got a {type(children)}"
                    )

            return process_api_item_list
        elif origin is None:
            if issubclass(annotation, ApiItem):

                def process_api_item(kwargs):
                    kwargs[field_name] = annotation.from_json(kwargs[field_name])

                return process_api_item

        initializer: Callable = custom_initializer or origin or annotation

        def process_default(kwargs):
            with contextlib.suppress(ValueError, TypeError):
                if kwargs[field_name] is not None:
                    kwargs[field_name] = initializer(kwargs[field_name])

        return process_default

    @classmethod
    def from_json(cls, data: dict[str, Any] | Any) -> "ApiItem_T":  # type: ignore
        """Process an object reveived as JSON and create the appro  ate ApiItem instance.

        If the ApiItem subclass is a dataclass then the data dictionary is processed
        and the resulting object should be correct based on the type hints for
        the fields in the dataclass. This includes all nested data as the incoming
        object is processed recursively.

        If the ApiItem is not a dataclass then the data dictionary is simply passed
        directly into the class constructor.

        Args:
            data (dict[str, Any]): A dictionary that has been produced (usually) from
                parsing a JSON document.

        Raises:
            ValueError: If the input data does not match the expected structure based on
               the dataclass's type hints.

        Returns:
            ApiItem: An initialized ApiItem

        """
        kwargs = {}
        for api_field in fields(cls):
            if api_field.name == "raw":
                continue
            if "json" in api_field.metadata and api_field.metadata["json"] in data:
                kwargs[api_field.name] = data[api_field.metadata["json"]]
            elif api_field.name in data:
                kwargs[api_field.name] = data[api_field.name]
            else:
                continue

            cls._api_item_annotations()[api_field.name](kwargs)
        instance = cls(**kwargs)  # type: ignore
        instance.raw = data
        return instance  # type: ignore

    def __post_init__(self):
        """Perform post-initialization updates."""
        if not hasattr(self, "raw"):
            self.raw = {}

    def replace(self, other: "ApiItem"):
        """Create a copy of the current object replacing non-None values from other into the new object."""
        new_item_data = {}
        for api_field in fields(self):
            if api_field.name == "raw":
                continue
            new_item_data[api_field.name] = getattr(self, api_field.name)
            new_value = getattr(other, api_field.name, None)
            if new_value is not None:
                new_item_data[api_field.name] = new_value
        new_item = self.__class__(**new_item_data)
        new_item.raw = deepcopy(getattr(self, "raw", {}))
        return new_item

    def to_json(self, output_fields: set[str] | None = None) -> dict[str, Any]:
        """Generate a dictionary suitable for marshaling to JSON.

        If the ApiItem is a dataclass, then this method will construct a dictionary
        of non-None fields named as either the field name (default) or using the json
        metadata provided in the dataclass field. If the ApiItem is not a dataclass
        then it is returned unchanged.

        Returns:
            dict[str, Any]: A dictionary that can be serialized as json

        """
        data = {}
        api_item_fields = [
            api_field
            for api_field in fields(self)
            if output_fields is None or api_field.name in output_fields
        ]
        for api_field in api_item_fields:
            if api_field.name == "raw":
                continue
            value = getattr(self, api_field.name)
            field_name = api_field.name
            if json_name := api_field.metadata.get("json"):
                field_name = json_name
            if isinstance(value, ApiItem):
                data[field_name] = value.to_json()
            elif (
                isinstance(value, list)
                and len(value) > 0
                and isinstance(value[0], ApiItem)
            ):
                data[field_name] = [item.to_json() for item in value]
            elif value is not None:
                data[field_name] = value
        # include original values from the raw data
        raw = {
            key: value
            for key, value in getattr(self, "raw", {}).items()
            if output_fields is None or key in output_fields
        }
        return {**raw, **data}


def json_field(
    json_key: str | None = None,
    custom_initializer: Callable[[Any], Any] | None = None,
    **kwargs,
):
    """Return a dataclass field with json metadata.

    This method will create a dataclass field that has metadata indicating
    the json object key for a given field. This provides a way to indicate
    that a dataclass field is named different in the json structure
    than it is in the dataclass itself.

    Args:
        json_key (str | None): The json object key to translate
        custom_initializer (Callable | None): A callable that is used for type conversion.
        kwargs (dict, Any): Keyword arguments passed along to the dataclass.field
            method. The most common is the `default` argument.

    Returns:
        Field: The initialized dataclass field

    """
    metadata = {}
    if json_key:
        metadata["json"] = json_key
    if custom_initializer:
        metadata["custom_initializer"] = custom_initializer
    return field(**kwargs, metadata=metadata)
