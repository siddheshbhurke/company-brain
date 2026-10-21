
import pytest

from app.policies.rule_engine import evaluate_refund


def test_large_refund_requires_manager_approval():
    result = evaluate_refund(
        refund_amount=75000,
        customer_valid=True,
        order_valid=True,
        eligible=True,
    )

    assert result["decision"] == "pending_approval"
    assert result["approval_required"] is True
    assert result["required_role"] == "Customer Operations Manager"
    assert result["execute_refund"] is False


def test_small_eligible_refund():
    result = evaluate_refund(
        refund_amount=40000,
        customer_valid=True,
        order_valid=True,
        eligible=True,
    )

    assert result["decision"] == "eligible_for_automatic_approval"
    assert result["approval_required"] is False
    assert result["execute_refund"] is False


def test_invalid_customer_is_rejected():
    result = evaluate_refund(
        refund_amount=40000,
        customer_valid=False,
        order_valid=True,
        eligible=True,
    )

    assert result["decision"] == "rejected"
    assert result["execute_refund"] is False


def test_invalid_order_is_rejected():
    result = evaluate_refund(
        refund_amount=40000,
        customer_valid=True,
        order_valid=False,
        eligible=True,
    )

    assert result["decision"] == "rejected"


def test_ineligible_order_is_rejected():
    result = evaluate_refund(
        refund_amount=40000,
        customer_valid=True,
        order_valid=True,
        eligible=False,
    )

    assert result["decision"] == "rejected"


def test_already_refunded_order_is_rejected():
    result = evaluate_refund(
        refund_amount=40000,
        customer_valid=True,
        order_valid=True,
        eligible=True,
        already_refunded=True,
    )

    assert result["decision"] == "rejected"


@pytest.mark.parametrize("amount", [0, -100, -50000])
def test_non_positive_refund_amount_is_rejected(amount):
    result = evaluate_refund(
        refund_amount=amount,
        customer_valid=True,
        order_valid=True,
        eligible=True,
    )

    assert result["decision"] == "rejected"
    assert result["execute_refund"] is False
