
from pathlib import Path
from typing import Any
import re
import json

from app.skills.skill_contract import load_skill_definition


PROJECT_ROOT = Path(__file__).resolve().parents[3]
GENERATED_SKILLS_DIR = PROJECT_ROOT / "skills" / "generated"


def get_skill_folder_name(skill_id: str) -> str:
    """Convert internal skill IDs into lowercase, hyphenated folder names."""
    return re.sub(r"[^a-z0-9]+", "-", skill_id.lower()).strip("-")


def render_skill_markdown(skill: dict[str, Any]) -> str:
    """Convert a validated skill definition into standard SKILL.md Markdown."""

    skill_name = get_skill_folder_name(skill["skill_id"])
    description = skill["description"].strip()
    display_name = skill["name"]

    # JSON-style quoting is valid for YAML strings and handles special characters.
    lines = [
        "---",
        f"name: {skill_name}",
        f"skill_id: {skill['skill_id']}",
        f"description: {json.dumps(description, ensure_ascii=False)}",
        "---",
        "",
        f"# {display_name}",
        "",
        description,
        "",
        "## Skill Metadata",
        "",
        f"- **Skill ID:** `{skill['skill_id']}`",
        f"- **Version:** `{skill.get('version', '1.0.0')}`",
        f"- **Risk Level:** {skill.get('risk_level', 'unspecified')}",
        f"- **Status:** {skill.get('status', 'draft')}",
        "",
        "## Inputs",
        "",
    ]

    inputs = skill.get("inputs", [])
    if inputs:
        lines.extend(f"- `{item}`" for item in inputs)
    else:
        lines.append("- No inputs specified.")

    lines.extend(["", "## Outputs", ""])

    outputs = skill.get("outputs", [])
    if outputs:
        lines.extend(f"- `{item}`" for item in outputs)
    else:
        lines.append("- No outputs specified.")

    lines.extend(["", "## Capabilities", ""])

    capabilities = skill.get("capabilities", [])
    if capabilities:
        lines.extend(f"- `{item}`" for item in capabilities)
    else:
        lines.append("- No capabilities specified.")

    lines.extend(["", "## Constraints", ""])

    constraints = skill.get("constraints", [])
    if constraints:
        lines.extend(f"- {item}" for item in constraints)
    else:
        lines.append("- No constraints specified.")

    lines.extend(["", "## Procedure", ""])

    for step in skill["steps"]:
        lines.extend([
            f"### Step {step['order']}: {step['name']}",
            "",
            f"**Action:** `{step['action']}`",
            "",
        ])

        tool_name = step.get("tool_name")
        if tool_name:
            lines.extend([
                f"**Tool:** `{tool_name}`",
                "",
            ])

    lines.extend([
        "## Execution Notes",
        "",
        "- Follow the steps in the defined order.",
        "- Use only authorized tools and approved company information.",
        "- Enforce applicable policies and approval requirements before actions.",
        "- Record execution outcomes through the authorized audit mechanism.",
        "- Stop and request clarification or approval when required information,",
        "  authorization, or policy decisions are missing.",
        "",
    ])

    return "\n".join(lines)


def compile_skill(skill_id: str) -> Path:
    """Validate a skill and write its generated SKILL.md artifact."""

    skill = load_skill_definition(skill_id)

    # The folder name and SKILL.md frontmatter name must match.
    folder_name = get_skill_folder_name(skill["skill_id"])
    output_dir = GENERATED_SKILLS_DIR / folder_name
    output_file = output_dir / "SKILL.md"

    safe_root = GENERATED_SKILLS_DIR.resolve()
    safe_output = output_file.resolve()

    if not safe_output.is_relative_to(safe_root):
        raise ValueError("Invalid skill output path.")

    output_dir.mkdir(parents=True, exist_ok=True)

    markdown = render_skill_markdown(skill)
    output_file.write_text(markdown, encoding="utf-8")

    return output_file
