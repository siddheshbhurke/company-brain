
from typing import Any

from app.policies.rule_engine import evaluate_refund
from app.skills.skill_loader import load_skill


def create_execution_plan(
    customer_id: str,
    order_id: str,
    refund_amount: float,
    customer_valid: bool,
    order_valid: bool,
    eligible: bool,
    already_refunded: bool = False,
    manager_approved: bool = False,
) -> dict[str, Any]:
    """
    Build a controlled execution plan.

    This function plans work only. It never executes external tools
    or issues a real refund.
    """

    skill = load_skill("process_refund")

    decision = evaluate_refund(
        refund_amount=refund_amount,
        customer_valid=customer_valid,
        order_valid=order_valid,
        eligible=eligible,
        already_refunded=already_refunded,
    )

    plan = {
        "skill_id": skill["skill_id"],
        "skill_version": skill["version"],
        "customer_id": customer_id,
        "order_id": order_id,
        "refund_amount": refund_amount,
        "decision": decision["decision"],
        "reason": decision["reason"],
        "status": "blocked",
        "approval_required": decision["approval_required"],
        "steps": [],
    }

    if decision["decision"] == "rejected":
        plan["status"] = "rejected"
        return plan

    approval_required = decision["approval_required"]

    for step in skill["steps"]:
        step_name = step["name"]

        if step_name == "request_manager_approval":
            if approval_required and not manager_approved:
                plan["steps"].append({
                    "name": step_name,
                    "status": "awaiting_approval",
                    "tool_name": step["tool_name"],
                })
                plan["status"] = "pending_approval"
                break

            if not approval_required:
                plan["steps"].append({
                    "name": step_name,
                    "status": "skipped",
                    "reason": "Approval is not required.",
                })
                continue

        if step_name == "execute_refund":
            if approval_required and not manager_approved:
                plan["steps"].append({
                    "name": step_name,
                    "status": "blocked",
                    "reason": "Manager approval has not been recorded.",
                })
                plan["status"] = "pending_approval"
                break

            # Even when approved, this planner only creates a plan.
            plan["steps"].append({
                "name": step_name,
                "status": "ready_for_execution",
                "tool_name": step["tool_name"],
            })
            continue

        plan["steps"].append({
            "name": step_name,
            "status": "ready",
            "tool_name": step["tool_name"],
        })

    if plan["status"] == "blocked" and (
        not approval_required or manager_approved
    ):
        plan["status"] = "ready_for_execution"

    return plan


if __name__ == "__main__":
    result = create_execution_plan(
        customer_id="CUST-1001",
        order_id="ORD-18291",
        refund_amount=75000,
        customer_valid=True,
        order_valid=True,
        eligible=True,
    )

    print("Company Brain — Execution Plan")
    print("-" * 35)
    print(f"Order: {result['order_id']}")
    print(f"Decision: {result['decision']}")
    print(f"Status: {result['status']}")
    print(f"Approval required: {result['approval_required']}")

    print("\nSteps:")
    for step in result["steps"]:
        print(f"- {step['name']}: {step['status']}")
