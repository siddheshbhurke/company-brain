
from typing import Any

from app.skills.skill_contract import load_skill_definition


def build_execution_plan(
    skill_id: str,
    inputs: dict[str, Any] | None = None,
    available_tools: set[str] | None = None,
) -> dict[str, Any]:
    """Build a generic execution plan without executing any actions."""

    skill = load_skill_definition(skill_id)
    supplied_inputs = inputs or {}

    required_inputs = skill.get("inputs", [])
    missing_inputs = [
    name
    for name in required_inputs
    if (
        name not in supplied_inputs
        or supplied_inputs[name] is None
        or (
            isinstance(supplied_inputs[name], str)
            and not supplied_inputs[name].strip()
        )
    )
]

    steps = []
    missing_tools = set()

    for step in skill["steps"]:
        tool_name = step.get("tool_name")

        if tool_name and available_tools is not None:
            if tool_name not in available_tools:
                missing_tools.add(tool_name)

        steps.append(
            {
                "order": step["order"],
                "name": step["name"],
                "action": step["action"],
                "tool_name": tool_name,
                "requires_tool_check": tool_name is not None,
            }
        )

    if missing_inputs:
        status = "blocked_missing_inputs"
    elif available_tools is not None and missing_tools:
        status = "blocked_missing_tools"
    else:
        status = "ready_for_review"

    return {
        "skill_id": skill["skill_id"],
        "skill_name": skill["name"],
        "skill_version": skill["version"],
        "status": status,
        "execution_started": False,
        "missing_inputs": missing_inputs,
        "missing_tools": sorted(missing_tools),
        "steps": steps,
        "constraints": skill.get("constraints", []),
        "risk_level": skill.get("risk_level", "unspecified"),
        "approval_policy": (
            "Must be evaluated by the governed runtime before execution."
        ),
    }
