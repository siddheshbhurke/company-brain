
import json
from datetime import date
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[3]
COMPANY_DATA_DIR = PROJECT_ROOT / "data" / "company"


def _load_json(filename: str) -> list[dict[str, Any]]:
    """Load a JSON list from the TechMart company data directory."""

    path = COMPANY_DATA_DIR / filename

    if not path.is_file():
        raise FileNotFoundError(f"Company data file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError(f"{filename} must contain a JSON list.")

    return data


def get_customer(customer_id: str) -> dict[str, Any] | None:
    """Find a customer by their unique customer ID."""

    customers = _load_json("customers.json")

    return next(
        (
            customer
            for customer in customers
            if customer.get("customer_id") == customer_id
        ),
        None,
    )


def get_order(order_id: str) -> dict[str, Any] | None:
    """Find an order by its unique order ID."""

    orders = _load_json("orders.json")

    return next(
        (
            order
            for order in orders
            if order.get("order_id") == order_id
        ),
        None,
    )


def validate_refund_request(
    customer_id: str,
    order_id: str,
    as_of_date: date | None = None,
) -> dict[str, Any]:
    """
    Validate a refund request using the existing TechMart JSON records.

    This function only validates and returns information.
    It does not approve or execute refunds.
    """

    customer = get_customer(customer_id)
    order = get_order(order_id)

    if customer is None:
        return {
            "valid": False,
            "reason": "Customer not found.",
            "customer": None,
            "order": order,
            "eligible": False,
            "already_refunded": False,
        }

    if order is None:
        return {
            "valid": False,
            "reason": "Order not found.",
            "customer": customer,
            "order": None,
            "eligible": False,
            "already_refunded": False,
        }

    if order.get("customer_id") != customer_id:
        return {
            "valid": False,
            "reason": "Order does not belong to the specified customer.",
            "customer": customer,
            "order": order,
            "eligible": False,
            "already_refunded": False,
        }

    refund_status = str(order.get("refund_status", "none")).lower()
    already_refunded = refund_status in {"refunded", "completed"}

    if already_refunded:
        return {
            "valid": False,
            "reason": "Order has already been refunded.",
            "customer": customer,
            "order": order,
            "eligible": False,
            "already_refunded": True,
        }

    if order.get("status") != "delivered":
        return {
            "valid": False,
            "reason": "Order has not been delivered.",
            "customer": customer,
            "order": order,
            "eligible": False,
            "already_refunded": False,
        }

    if order.get("returnable") is not True:
        return {
            "valid": False,
            "reason": "Order is not returnable.",
            "customer": customer,
            "order": order,
            "eligible": False,
            "already_refunded": False,
        }

    delivery_date = date.fromisoformat(order["delivery_date"])
    reference_date = as_of_date or date.today()
    days_since_delivery = (reference_date - delivery_date).days

    if days_since_delivery < 0:
        return {
            "valid": False,
            "reason": "Delivery date is in the future.",
            "customer": customer,
            "order": order,
            "eligible": False,
            "already_refunded": False,
        }

    if days_since_delivery > 30:
        return {
            "valid": False,
            "reason": "Order is outside the 30-day refund window.",
            "customer": customer,
            "order": order,
            "eligible": False,
            "already_refunded": False,
        }

    return {
        "valid": True,
        "reason": "Customer, order, and basic refund eligibility checks passed.",
        "customer": customer,
        "order": order,
        "eligible": True,
        "already_refunded": False,
        "days_since_delivery": days_since_delivery,
    }
