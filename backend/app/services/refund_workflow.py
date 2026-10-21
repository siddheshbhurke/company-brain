
from datetime import date
from typing import Any

from app.services.techmart_service import validate_refund_request
from app.skills.execution_planner import create_execution_plan


def plan_refund_from_company_data(
    customer_id: str,
    order_id: str,
    as_of_date: date | None = None,
) -> dict[str, Any]:
    """
    Build a refund plan using the actual TechMart JSON records.

    This workflow validates company data before creating a plan.
    It never executes a real refund.
    """

    validation = validate_refund_request(
        customer_id=customer_id,
        order_id=order_id,
        as_of_date=as_of_date,
    )

    if not validation["valid"]:
        return {
            "customer_id": customer_id,
            "order_id": order_id,
            "status": "rejected",
            "reason": validation["reason"],
            "steps": [],
        }

    order = validation["order"]

    plan = create_execution_plan(
        customer_id=customer_id,
        order_id=order_id,
        refund_amount=order["amount"],
        customer_valid=True,
        order_valid=True,
        eligible=validation["eligible"],
        already_refunded=validation["already_refunded"],
    )

    plan["validation"] = {
        "valid": validation["valid"],
        "reason": validation["reason"],
        "days_since_delivery": validation["days_since_delivery"],
    }

    return plan


if __name__ == "__main__":
    result = plan_refund_from_company_data(
        customer_id="CUST-1001",
        order_id="ORD-18291",
        as_of_date=date(2026, 9, 20),
    )

    print("Company Brain — Data-backed Refund Plan")
    print("-" * 42)
    print(f"Order: {result['order_id']}")
    print(f"Status: {result['status']}")
    print(f"Reason: {result['reason']}")
    print(f"Approval required: {result.get('approval_required', False)}")

    print("\nSteps:")
    for step in result["steps"]:
        print(f"- {step['name']}: {step['status']}")

