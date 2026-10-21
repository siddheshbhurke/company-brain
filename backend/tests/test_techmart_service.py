
from datetime import date

from app.services.techmart_service import (
    get_customer,
    get_order,
    validate_refund_request,
)


def test_existing_customer_is_found():
    customer = get_customer("CUST-1001")

    assert customer is not None
    assert customer["name"] == "Aarav Mehta"


def test_existing_order_is_found():
    order = get_order("ORD-18291")

    assert order is not None
    assert order["customer_id"] == "CUST-1001"
    assert order["amount"] == 75000


def test_unknown_customer_is_rejected():
    result = validate_refund_request(
        "CUST-9999",
        "ORD-18291",
        as_of_date=date(2026, 9, 20),
    )

    assert result["valid"] is False
    assert result["eligible"] is False


def test_order_owned_by_another_customer_is_rejected():
    result = validate_refund_request(
        "CUST-1002",
        "ORD-18291",
        as_of_date=date(2026, 9, 20),
    )

    assert result["valid"] is False
    assert "does not belong" in result["reason"]


def test_refund_within_30_days_is_eligible():
    result = validate_refund_request(
        "CUST-1001",
        "ORD-18291",
        as_of_date=date(2026, 9, 20),
    )

    assert result["valid"] is True
    assert result["eligible"] is True
    assert result["days_since_delivery"] == 10


def test_refund_outside_30_days_is_rejected():
    result = validate_refund_request(
        "CUST-1003",
        "ORD-18293",
        as_of_date=date(2026, 9, 30),
    )

    assert result["valid"] is False
    assert "30-day" in result["reason"]


def test_non_returnable_order_is_rejected():
    result = validate_refund_request(
        "CUST-1005",
        "ORD-18295",
        as_of_date=date(2026, 9, 20),
    )

    assert result["valid"] is False
    assert result["eligible"] is False
