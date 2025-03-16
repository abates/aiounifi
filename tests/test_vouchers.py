"""Test voucher configuration API.

pytest --cov-report term-missing --cov=aiounifi.voucher tests/test_vouchers.py
"""

from datetime import timedelta
from typing import Any

import pytest

from aiounifi.interfaces.vouchers import Vouchers
from aiounifi.models.voucher import Voucher, VoucherCode

from tests.conftest import assert_handler_request


def test_voucher_code():
    """Confirm the behavior of VoucherCode."""
    code = VoucherCode("0123456789")
    assert str(code) == "01234-56789"

    voucher = Voucher.from_json({"id": 1, "duration": 1, "code": "0123456789"})
    assert type(voucher.code) is VoucherCode
    assert str(voucher.code) == "01234-56789"


@pytest.mark.parametrize(
    ("method_name", "method_args", "expected_request", "expected_error"),
    [
        (
            "create",
            {
                "voucher": Voucher(
                    id="traffic_rule_1",
                    duration=timedelta(seconds=3600),
                    quota=0,
                    note="Unit Testing",
                    qos_usage_quota=1000,
                    qos_rate_max_up=5000,
                    qos_rate_max_down=2000,
                ),
            },
            {
                "method": "post",
                "endpoint": Vouchers.create_endpoint,
                "api_item": Voucher(
                    id="traffic_rule_1",
                    duration=timedelta(seconds=3600),
                    quota=0,
                    note="Unit Testing",
                    qos_usage_quota=1000,
                    qos_rate_max_up=5000,
                    qos_rate_max_down=2000,
                ),
                "data": {
                    "cmd": "create-voucher",
                    "n": 1,
                    "quota": 0,
                    "expire_number": 60,
                    "expire_unit": 1,
                    "bytes": 1000,
                    "up": 5000,
                    "down": 2000,
                    "note": "Unit Testing",
                },
            },
            None,
        ),
        (
            "delete",
            {
                "voucher": Voucher(
                    id="657e370a4543a555901865c7",
                    duration=timedelta(seconds=3600),
                ),
            },
            {
                "method": "post",
                "endpoint": Vouchers.create_endpoint,
                "api_item": Voucher(
                    id="657e370a4543a555901865c7",
                    duration=timedelta(seconds=3600),
                ),
                "data": {
                    "cmd": "delete-voucher",
                    "_id": "657e370a4543a555901865c7",
                },
            },
            None,
        ),
    ],
)
async def test_vouchers(
    method_name: str,
    method_args: dict[str, Any],
    expected_request: dict[str, Any],
    expected_error: type[Exception] | None,
):
    """Test device interface methods."""
    await assert_handler_request(
        Vouchers,
        method_name,
        method_args,
        expected_request,
        expected_error,
    )
