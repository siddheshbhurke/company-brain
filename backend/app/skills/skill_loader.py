
from pathlib import Path
from typing import Any

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[3]
SKILL_DIRECTORY = PROJECT_ROOT / "skills"


def load_skill(skill_id: str) -> dict[str, Any]:
    """Load a skill definition from the project's skills directory."""

    if not skill_id.replace("_", "").isalnum():
        raise ValueError("Invalid skill ID.")

    skill_path = SKILL_DIRECTORY / f"{skill_id}.yaml"

    if not skill_path.is_file():
        raise FileNotFoundError(f"Skill not found: {skill_id}")

    with skill_path.open("r", encoding="utf-8") as file:
        skill = yaml.safe_load(file)

    validate_skill(skill)
    return skill


def validate_skill(skill: dict[str, Any]) -> None:
    """Check the basic structure and safety constraints of a skill."""

    if not isinstance(skill, dict):
        raise ValueError("Skill definition must be a YAML mapping.")

    for field in ("skill_id", "name", "version", "steps", "safety"):
        if field not in skill:
            raise ValueError(f"Missing required field: {field}")

    if not isinstance(skill["steps"], list) or not skill["steps"]:
        raise ValueError("A skill must contain at least one step.")

    orders = []

    for step in skill["steps"]:
        for field in ("order", "name", "action", "tool_name"):
            if field not in step:
                raise ValueError(f"Skill step is missing: {field}")

        orders.append(step["order"])

    if len(orders) != len(set(orders)):
        raise ValueError("Skill step order numbers must be unique.")

    if orders != sorted(orders):
        raise ValueError("Skill steps must be ordered by their order field.")

    safety = skill["safety"]

    if safety.get("execute_refund_before_validation") is not False:
        raise ValueError("Refund execution before validation must be disabled.")

    if safety.get("execute_refund_before_required_approval") is not False:
        raise ValueError("Refund execution before approval must be disabled.")


if __name__ == "__main__":
    refund_skill = load_skill("process_refund")

    print(f"Skill loaded: {refund_skill['name']}")
    print(f"Version: {refund_skill['version']}")
    print(f"Total steps: {len(refund_skill['steps'])}")
    print("Skill validation: PASSED")
