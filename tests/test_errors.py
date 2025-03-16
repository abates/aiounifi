from http import HTTPStatus
from unittest.mock import Mock

import pytest

from aiounifi import errors


@pytest.mark.parametrize(
    ("version", "response_data", "expected_error"),
    [
        (1, {"meta": {"rc": "error", "msg": "api.err.Invalid"}}, errors.Unauthorized),
        (2, {"errorCode": 123, "message": "api.err.Invalid"}, errors.Unauthorized),
        (
            1,
            {"meta": {"rc": "error", "msg": "api.err.UnknownErrorCode"}},
            errors.AiounifiException,
        ),
        (1, {}, None),
        (2, {}, None),
    ],
)
def test_raise_for_unifi_error(version, response_data, expected_error):
    """Verify behavior of the `raise_for_unifi_error` method."""
    if expected_error is not None:
        with pytest.raises(expected_error):
            errors.raise_for_unifi_error(version, response_data)
    else:
        # No error should be raised
        errors.raise_for_unifi_error(version, response_data)


@pytest.mark.parametrize(
    ("client_response", "expected_error"),
    [
        (Mock(status=HTTPStatus.UNAUTHORIZED), errors.LoginRequired),
        (Mock(status=HTTPStatus.OK), None),
    ],
)
async def test_raise_for_status(client_response, expected_error):
    """Verify behavior of the `raise_for_unifi_error` method."""
    if expected_error is not None:
        with pytest.raises(expected_error):
            await errors.raise_for_status(client_response)
    else:
        # No error should be raised
        await errors.raise_for_status(client_response)
