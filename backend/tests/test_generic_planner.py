
from app.skills.generic_planner import build_execution_plan
from app.skills.skill_registry import discover_skills, get_skill


def test_registry_discovers_both_skills():
    skills = discover_skills()
    skill_ids = {skill["skill_id"] for skill in skills}

    assert "process_refund" in skill_ids
    assert "employee_onboarding" in skill_ids


def test_registry_returns_skill_definition():
    skill = get_skill("employee_onboarding")

    assert skill["name"] == "Employee Onboarding"
    assert len(skill["steps"]) == 5


def test_onboarding_plan_reports_missing_inputs():
    plan = build_execution_plan("employee_onboarding")

    assert plan["status"] == "blocked_missing_inputs"
    assert set(plan["missing_inputs"]) == {
        "employee_id",
        "start_date",
        "department",
    }
    assert plan["execution_started"] is False


def test_onboarding_plan_checks_tool_availability():
    plan = build_execution_plan(
        "employee_onboarding",
        inputs={
            "employee_id": "EMP-TEST",
            "start_date": "2026-11-01",
            "department": "Engineering",
        },
        available_tools=set(),
    )

    assert plan["status"] == "blocked_missing_tools"
    assert "employee_lookup" in plan["missing_tools"]
    assert "task_management" in plan["missing_tools"]
    assert plan["execution_started"] is False


def test_plan_can_be_built_for_different_domains():
    refund_plan = build_execution_plan("process_refund")
    onboarding_plan = build_execution_plan("employee_onboarding")

    assert refund_plan["skill_id"] == "process_refund"
    assert onboarding_plan["skill_id"] == "employee_onboarding"
    assert refund_plan["steps"]
    assert onboarding_plan["steps"]


def test_complete_onboarding_plan_is_ready_for_review():
    skill = get_skill("employee_onboarding")

    tools = {
        step["tool_name"]
        for step in skill["steps"]
        if step.get("tool_name")
    }

    plan = build_execution_plan(
        "employee_onboarding",
        inputs={
            "employee_id": "EMP-TEST",
            "start_date": "2026-11-01",
            "department": "Engineering",
        },
        available_tools=tools,
    )

    assert plan["status"] == "ready_for_review"
    assert plan["missing_inputs"] == []
    assert plan["missing_tools"] == []
    assert plan["execution_started"] is False
