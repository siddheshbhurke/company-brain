
from decimal import Decimal
from typing import Any


REFUND_THRESHOLD = Decimal("50000")


def evaluate_refund(
    refund_amount: float,
    customer_valid: bool,
    order_valid: bool,
    eligible: bool,
    already_refunded: bool = False,
) -> dict[str, Any]:
    """
    Evaluate a TechMart refund request against
    the current prototype's refund rules.

    This function decides whether approval is required.
    It does not execute a refund.
    """

    amount = Decimal(str(refund_amount))

    if amount <= 0:
        return {
            "decision": "rejected",
            "reason": "Refund amount must be greater than zero.",
            "approval_required": False,
            "execute_refund": False,
        }

    if not customer_valid:
        return {
            "decision": "rejected",
            "reason": "Customer validation failed.",
            "approval_required": False,
            "execute_refund": False,
        }

    if not order_valid:
        return {
            "decision": "rejected",
            "reason": "Order validation failed.",
            "approval_required": False,
            "execute_refund": False,
        }

    if not eligible:
        return {
            "decision": "rejected",
            "reason": "Order is not eligible for a refund.",
            "approval_required": False,
            "execute_refund": False,
        }

    if already_refunded:
        return {
            "decision": "rejected",
            "reason": "Order has already been refunded.",
            "approval_required": False,
            "execute_refund": False,
        }

    if amount > REFUND_THRESHOLD:
        return {
            "decision": "pending_approval",
            "reason": (
                "Refund exceeds INR 50000. "
                "Customer Operations Manager approval is required."
            ),
            "approval_required": True,
            "required_role": "Customer Operations Manager",
            "execute_refund": False,
        }

    return {
        "decision": "eligible_for_automatic_approval",
        "reason": (
            "Refund is within the automatic approval threshold, "
            "subject to all eligibility checks."
        ),
        "approval_required": False,
        "execute_refund": False,
    }


if __name__ == "__main__":
    result = evaluate_refund(
        refund_amount=75000,
        customer_valid=True,
        order_valid=True,
        eligible=True,
    )

    print("Refund Rule Evaluation")
    print("-" * 30)

    for key, value in result.items():
        print(f"{key}: {value}")
