"""Setup common test helpers."""

from collections.abc import Callable
from inspect import Parameter, signature
from typing import Any
from unittest.mock import AsyncMock, Mock

import pytest

from aiounifi.client import UnifiClient
from aiounifi.interfaces.api_handlers import APIHandler
from aiounifi.models.api import ApiResponse


def bind_test_method(
    handler, method_name, request_args
) -> tuple[Callable, tuple[Any], dict[str, Any]]:
    method = getattr(handler, method_name)
    sig = signature(method)

    kwargs = {}
    args = []
    for name, parameter in sig.parameters.items():
        if name in request_args:
            if parameter.kind == Parameter.POSITIONAL_OR_KEYWORD:
                args.append(request_args.pop(name))
            elif parameter.kind == Parameter.KEYWORD_ONLY:
                kwargs[name] = request_args.pop(name)
            elif parameter.kind == Parameter.POSITIONAL_ONLY:
                args.append(request_args.pop(name))
            elif parameter.kind == Parameter.VAR_POSITIONAL:
                args.extend(request_args.pop(name))
            else:
                raise ValueError(str(parameter))
        elif parameter.kind == Parameter.VAR_KEYWORD and request_args:
            kwargs.update(request_args)
            request_args = {}
        elif parameter.default is not Parameter.empty:
            args.append(parameter.default)
    assert len(request_args) == 0, (
        f"Unexpected request arguments {','.join(request_args.keys())}"
    )
    bound_arguments = sig.bind(*args, **kwargs)
    return method, bound_arguments.args, bound_arguments.kwargs


async def assert_handler_request(
    handler_class: type[APIHandler],
    method_name: str,
    method_args: dict[str, Any],
    expected_request: dict[str, Any],
    expected_error: type[Exception] | None,
):
    """Test device interface methods.

    The expected_request should be a dictionary of keyword arguments to check in the
    `endpoint_request` call. Only those keys that are present in the `expected_request`
    dictionary will be checked in the call.
    """

    client = UnifiClient(Mock)
    client.endpoint_request = AsyncMock(return_value=ApiResponse(meta={}, data=[]))
    handler = handler_class(client)
    method, args, kwargs = bind_test_method(handler, method_name, method_args)

    if expected_error:
        with pytest.raises(expected_error):
            await method(*args, **kwargs)
        client.endpoint_request.assert_not_called()
    else:
        await method(*args, **kwargs)
        got_kwargs = client.endpoint_request.call_args.kwargs
        for key, value in expected_request.items():
            assert got_kwargs[key] == value, (
                f"Expected {handler_class.__name__}.{method.__name__} arg {key} to be {value} but got {got_kwargs[key]}"
            )
