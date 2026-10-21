
import copy

import pytest

from app.skills.skill_loader import load_skill, validate_skill


def test_refund_skill_loads_successfully():
    skill = load_skill("process_refund")

    assert skill["skill_id"] == "process_refund"
    assert skill["name"] == "Process Customer Refund"
    assert len(skill["steps"]) == 9


def test_skill_steps_are_ordered():
    skill = load_skill("process_refund")

    orders = [step["order"] for step in skill["steps"]]

    assert orders == sorted(orders)
    assert len(orders) == len(set(orders))


def test_refund_execution_before_validation_is_rejected():
    skill = load_skill("process_refund")
    invalid_skill = copy.deepcopy(skill)

    invalid_skill["safety"]["execute_refund_before_validation"] = True

    with pytest.raises(ValueError):
        validate_skill(invalid_skill)


def test_refund_execution_before_approval_is_rejected():
    skill = load_skill("process_refund")
    invalid_skill = copy.deepcopy(skill)

    invalid_skill["safety"]["execute_refund_before_required_approval"] = True

    with pytest.raises(ValueError):
        validate_skill(invalid_skill)


def test_duplicate_step_orders_are_rejected():
    skill = load_skill("process_refund")
    invalid_skill = copy.deepcopy(skill)

    invalid_skill["steps"][1]["order"] = invalid_skill["steps"][0]["order"]

    with pytest.raises(ValueError):
        validate_skill(invalid_skill)


def test_missing_required_field_is_rejected():
    skill = load_skill("process_refund")
    invalid_skill = copy.deepcopy(skill)

    del invalid_skill["name"]

    with pytest.raises(ValueError):
        validate_skill(invalid_skill)


def test_empty_steps_are_rejected():
    skill = load_skill("process_refund")
    invalid_skill = copy.deepcopy(skill)

    invalid_skill["steps"] = []

    with pytest.raises(ValueError):
        validate_skill(invalid_skill)
