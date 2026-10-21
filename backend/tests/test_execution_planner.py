
import pytest

from app.skills.execution_planner import create_execution_plan


def make_plan(**overrides):
    inputs = {
        "customer_id": "CUST-1001",
        "order_id": "ORD-18291",
        "refund_amount": 75000,
        "customer_valid": True,
        "order_valid": True,
        "eligible": True,
    }
    inputs.update(overrides)
    return create_execution_plan(**inputs)


def test_large_refund_pauses_for_approval():
    plan = make_plan()

    assert plan["status"] == "pending_approval"
    assert plan["approval_required"] is True
    assert plan["steps"][-1]["name"] == "request_manager_approval"
    assert plan["steps"][-1]["status"] == "awaiting_approval"


def test_refund_execution_is_not_reached_before_approval():
    plan = make_plan()

    step_names = [step["name"] for step in plan["steps"]]

    assert "execute_refund" not in step_names


def test_invalid_customer_rejects_plan():
    plan = make_plan(customer_valid=False)

    assert plan["status"] == "rejected"
    assert plan["steps"] == []


def test_invalid_order_rejects_plan():
    plan = make_plan(order_valid=False)

    assert plan["status"] == "rejected"
    assert plan["steps"] == []


def test_ineligible_order_rejects_plan():
    plan = make_plan(eligible=False)

    assert plan["status"] == "rejected"
    assert plan["steps"] == []


def test_already_refunded_order_rejects_plan():
    plan = make_plan(already_refunded=True)

    assert plan["status"] == "rejected"
    assert plan["steps"] == []


def test_small_refund_does_not_require_manager_approval():
    plan = make_plan(refund_amount=40000)

    assert plan["decision"] == "eligible_for_automatic_approval"
    assert plan["approval_required"] is False
    assert plan["status"] == "ready_for_execution"

    execution_steps = [
        step for step in plan["steps"]
        if step["name"] == "execute_refund"
    ]
    assert len(execution_steps) == 1
    assert execution_steps[0]["status"] == "ready_for_execution"


def test_approved_large_refund_can_be_planned():
    plan = make_plan(manager_approved=True)

    assert plan["status"] == "ready_for_execution"

    execution_steps = [
        step for step in plan["steps"]
        if step["name"] == "execute_refund"
    ]
    assert len(execution_steps) == 1
    assert execution_steps[0]["status"] == "ready_for_execution"
