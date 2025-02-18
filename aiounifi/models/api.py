"""API management class and base class for the different end points."""

from abc import ABC
from collections.abc import Mapping
import contextlib
from dataclasses import dataclass, field, fields, is_dataclass
from types import UnionType
from typing import Any, Protocol, TypeVar, get_args, get_origin, get_type_hints

import orjson

from ..errors import (
    AiounifiException,
    LoginRequired,
    NoPermission,
    TwoFaTokenRequired,
    Unauthorized,
)

ERRORS = {
    "api.err.Invalid": Unauthorized,
    "api.err.LoginRequired": LoginRequired,
    "api.err.NoPermission": NoPermission,
    "api.err.Ubic2faTokenRequired": TwoFaTokenRequired,
}


@dataclass
class ApiResponse:
    """Common response."""

    meta: dict[str, Any] = field(default_factory=dict)
    data: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ApiRequest:
    """Data class with required properties of a request."""

    method: str
    path: str
    data: Mapping[str, Any] | None = None

    def full_path(self, site: str, is_unifi_os: bool) -> str:
        """Create url to work with a specific controller."""
        if is_unifi_os:
            return f"/proxy/network/api/s/{site}{self.path}"
        return f"/api/s/{site}{self.path}"

    def decode(self, raw: bytes) -> ApiResponse:
        """Put data, received from the unifi controller, into a TypedApiResponse."""
        data: ApiResponse = orjson.loads(raw)

        if "meta" in data and data["meta"]["rc"] == "error":
            raise ERRORS.get(data["meta"]["msg"], AiounifiException)(data)

        data = ApiResponse(**data)
        return data


@dataclass
class ApiRequestV2(ApiRequest):
    """Data class with required properties of a V2 API request."""

    def full_path(self, site: str, is_unifi_os: bool) -> str:
        """Create url to work with a specific controller."""
        if is_unifi_os:
            return f"/proxy/network/v2/api/site/{site}{self.path}"
        return f"/v2/api/site/{site}{self.path}"

    def decode(self, raw: bytes) -> ApiResponse:
        """Put data, received from the unifi controller, into a TypedApiResponse."""
        data = orjson.loads(raw)

        if "errorCode" in data:
            raise ERRORS.get(data["message"], AiounifiException)(data)

        return ApiResponse(
            meta={"rc": "ok", "msg": ""},
            data=data if isinstance(data, list) else [data],
        )


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


T = TypeVar("T", bound="ApiItem")


class ApiItem(ABC):
    """Base class for all end points using APIItems class."""

    def __init__(self, raw: Any) -> None:
        """Initialize API item."""
        self.raw = raw

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
            annotation, origin, args = _get_annotation(annotations[api_field.name])
            api_item_annotations[api_field.name] = (  # type: ignore
                cls._generate_field_processor(api_field.name, annotation, origin, args)
            )

        return api_item_annotations

    @staticmethod
    def _generate_field_processor(
        field_name: str, annotation: type, origin: type, args: tuple[Any, ...]
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

        if origin is None:
            origin = annotation

        def process_default(kwargs):
            with contextlib.suppress(ValueError, TypeError):
                if kwargs[field_name] is not None:
                    kwargs[field_name] = origin(kwargs[field_name])

        return process_default

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "T":
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
        if is_dataclass(cls):
            kwargs = {}
            for field in fields(cls):
                if "json" in field.metadata and field.metadata["json"] in data:
                    kwargs[field.name] = data[field.metadata["json"]]
                elif field.name in data:
                    kwargs[field.name] = data[field.name]
                else:
                    continue

                cls._api_item_annotations()[field.name](kwargs)
            instance = cls(**kwargs)
            instance.raw = data
            return instance
        return cls(data)

    def to_json(self):
        """Generate a dictionary suitable for marshaling to JSON.

        If the ApiItem is a dataclass, then this method will construct a dictionary
        of non-None fields named as either the field name (default) or using the json
        metadata provided in the dataclass field. If the ApiItem is not a dataclass
        then it is returned unchanged.

        Returns:
            dict[str, Any]: A dictionary that can be serialized as json

        """
        if is_dataclass(self):
            data = {}
            for field in fields(self):
                value = getattr(self, field.name)
                if isinstance(value, ApiItem):
                    data[field.name] = value.to_json()
                elif value is not None:
                    data[field.name] = value
            return data
        return self


def json_field(json_key: str, **kwargs):
    """Return a dataclass field with json metadata.

    This method will create a dataclass field that has metadata indicating
    the json object key for a given field. This provides a way to indicate
    that a dataclass field is named different in the json structure
    than it is in the dataclass itself.

    Args:
        json_key (str): The json object key to translate
        kwargs (dict, Any): Keyword arguments passed along to the dataclass.field
            method. The most common is the `default` argument.

    Returns:
        Field: The initialized dataclass field

    """
    return field(**kwargs, metadata={"json": json_key})
