
from pathlib import Path
from typing import Any
import re

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[3]
SKILL_DIRECTORY = PROJECT_ROOT / "skills"


def validate_skill_contract(skill: dict[str, Any]) -> None:
    """Validate a domain-independent skill definition."""

    if not isinstance(skill, dict):
        raise ValueError("Skill must be a YAML mapping.")

    required_fields = (
        "skill_id",
        "name",
        "version",
        "description",
        "steps",
    )

    for field in required_fields:
        if field not in skill:
            raise ValueError(f"Missing required field: {field}")

    skill_id = skill["skill_id"]

    if not isinstance(skill_id, str) or not re.fullmatch(
        r"[a-z0-9]+(?:[-_][a-z0-9]+)*", skill_id
    ):
        raise ValueError("Invalid skill ID.")

    for field in ("name", "version", "description"):
        if not isinstance(skill[field], str) or not skill[field].strip():
            raise ValueError(f"{field} must be a non-empty string.")

    steps = skill["steps"]

    if not isinstance(steps, list) or not steps:
        raise ValueError("A skill must contain at least one step.")

    orders = []

    for step in steps:
        if not isinstance(step, dict):
            raise ValueError("Every skill step must be a mapping.")

        for field in ("order", "name", "action"):
            if field not in step:
                raise ValueError(f"Skill step is missing: {field}")

        if type(step["order"]) is not int or step["order"] < 1:
            raise ValueError("Step order must be a positive integer.")

        for field in ("name", "action"):
            if not isinstance(step[field], str) or not step[field].strip():
                raise ValueError(f"Step {field} must be a non-empty string.")

        tool_name = step.get("tool_name")

        if tool_name is not None and not isinstance(tool_name, str):
            raise ValueError("tool_name must be a string when provided.")

        orders.append(step["order"])

    if len(orders) != len(set(orders)):
        raise ValueError("Step order numbers must be unique.")

    if orders != sorted(orders):
        raise ValueError("Steps must be ordered by their order field.")

    for field in ("capabilities", "constraints"):
        value = skill.get(field, [])

        if not isinstance(value, list):
            raise ValueError(f"{field} must be a list.")

        if not all(isinstance(item, str) for item in value):
            raise ValueError(f"Every {field} entry must be a string.")


def load_skill_definition(skill_id: str) -> dict[str, Any]:
    """Load and validate any skill YAML file by its ID."""

    if not isinstance(skill_id, str) or not re.fullmatch(
        r"[a-z0-9]+(?:[-_][a-z0-9]+)*", skill_id
    ):
        raise ValueError("Invalid skill ID.")

    skill_path = SKILL_DIRECTORY / f"{skill_id}.yaml"

    if not skill_path.is_file():
        raise FileNotFoundError(f"Skill not found: {skill_id}")

    with skill_path.open("r", encoding="utf-8") as file:
        skill = yaml.safe_load(file)

    validate_skill_contract(skill)

    return skill
