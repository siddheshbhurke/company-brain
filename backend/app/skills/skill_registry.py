
from typing import Any

from app.skills.skill_contract import (
    SKILL_DIRECTORY,
    load_skill_definition,
)


def discover_skills() -> list[dict[str, Any]]:
    """Discover and validate all available skill definitions."""

    discovered = []

    if not SKILL_DIRECTORY.is_dir():
        return discovered

    for skill_file in sorted(SKILL_DIRECTORY.glob("*.yaml")):
        skill_id = skill_file.stem
        skill = load_skill_definition(skill_id)

        discovered.append(
            {
                "skill_id": skill["skill_id"],
                "name": skill["name"],
                "version": skill["version"],
                "description": skill["description"].strip(),
                "risk_level": skill.get("risk_level", "unspecified"),
                "status": skill.get("status", "draft"),
                "step_count": len(skill["steps"]),
            }
        )

    return discovered


def get_skill(skill_id: str) -> dict[str, Any]:
    """Retrieve one skill by its ID."""

    return load_skill_definition(skill_id)
