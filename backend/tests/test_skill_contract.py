
import copy

import pytest

from app.skills.skill_contract import (
    load_skill_definition,
    validate_skill_contract,
)


def test_existing_refund_skill_matches_generic_contract():
    skill = load_skill_definition("process_refund")

    assert skill["skill_id"] == "process_refund"
    assert skill["steps"]


def test_employee_onboarding_skill_matches_generic_contract():
    skill = load_skill_definition("employee_onboarding")

    assert skill["skill_id"] == "employee_onboarding"
    assert len(skill["steps"]) == 5


def test_generic_contract_accepts_different_domains():
    for skill_id in ("process_refund", "employee_onboarding"):
        skill = load_skill_definition(skill_id)
        validate_skill_contract(skill)


def test_duplicate_step_orders_are_rejected():
    skill = load_skill_definition("employee_onboarding")
    invalid_skill = copy.deepcopy(skill)

    invalid_skill["steps"][1]["order"] = 1

    with pytest.raises(ValueError):
        validate_skill_contract(invalid_skill)


def test_missing_step_action_is_rejected():
    skill = load_skill_definition("employee_onboarding")
    invalid_skill = copy.deepcopy(skill)

    del invalid_skill["steps"][0]["action"]

    with pytest.raises(ValueError):
        validate_skill_contract(invalid_skill)


def test_empty_steps_are_rejected():
    skill = load_skill_definition("employee_onboarding")
    invalid_skill = copy.deepcopy(skill)

    invalid_skill["steps"] = []

    with pytest.raises(ValueError):
        validate_skill_contract(invalid_skill)


def test_missing_description_is_rejected():
    skill = load_skill_definition("employee_onboarding")
    invalid_skill = copy.deepcopy(skill)

    del invalid_skill["description"]

    with pytest.raises(ValueError):
        validate_skill_contract(invalid_skill)
