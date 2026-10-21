
from pathlib import Path
from typing import Any

from app.skills.skill_contract import load_skill_definition


PROJECT_ROOT = Path(__file__).resolve().parents[3]
GENERATED_SKILLS_DIR = PROJECT_ROOT / "skills" / "generated"


def render_skill_markdown(skill: dict[str, Any]) -> str:
    """Convert a validated skill definition into standardized Markdown."""

    lines = [
        "---",
        f"skill_id: {skill['skill_id']}",
        f"name: {skill['name']}",
        f"version: {skill['version']}",
        f"description: {skill['description'].strip()}",
        f"risk_level: {skill.get('risk_level', 'unspecified')}",
        f"status: {skill.get('status', 'draft')}",
        "---",
        "",
        f"# {skill['name']}",
        "",
        skill["description"].strip(),
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
        lines.extend(
            [
                f"### Step {step['order']}: {step['name']}",
                "",
                f"**Action:** `{step['action']}`",
                "",
            ]
        )

        tool_name = step.get("tool_name")
        if tool_name:
            lines.extend([f"**Tool:** `{tool_name}`", ""])

    lines.extend(
        [
            "## Execution Notes",
            "",
            "- Follow the steps in the defined order.",
            "- Use only authorized tools and approved company information.",
            "- Enforce applicable policies and approval requirements before actions.",
            "- Record execution outcomes through the authorized audit mechanism.",
            "- Stop and request clarification or approval when required information,",
            "  authorization, or policy decisions are missing.",
            "",
        ]
    )

    return "\n".join(lines)


def compile_skill(skill_id: str) -> Path:
    """Validate a skill and write its generated SKILL.md artifact."""

    # The loader validates the ID, finds the YAML file, and validates its schema.
    skill = load_skill_definition(skill_id)

    # Build the destination only from the validated skill ID.
    output_dir = GENERATED_SKILLS_DIR / skill["skill_id"]
    output_file = output_dir / "SKILL.md"

    # Ensure the resolved destination remains inside the generated skills directory.
    safe_root = GENERATED_SKILLS_DIR.resolve()
    safe_output = output_file.resolve()

    if not safe_output.is_relative_to(safe_root):
        raise ValueError("Invalid skill output path.")

    output_dir.mkdir(parents=True, exist_ok=True)

    markdown = render_skill_markdown(skill)
    output_file.write_text(markdown, encoding="utf-8")

    return output_file
