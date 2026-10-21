
from pathlib import Path

import pytest

from app.skills.skill_compiler import (
    GENERATED_SKILLS_DIR,
    compile_skill,
    render_skill_markdown,
)
from app.skills.skill_contract import load_skill_definition


def test_refund_skill_compiles():
    output = compile_skill("process_refund")

    assert output.name == "SKILL.md"
    assert output.is_file()

    content = output.read_text(encoding="utf-8")
    assert "# Process Customer Refund" in content
    assert "## Procedure" in content


def test_employee_onboarding_skill_compiles():
    output = compile_skill("employee_onboarding")

    assert output.is_file()

    content = output.read_text(encoding="utf-8")
    assert "Employee Onboarding" in content
    assert "retrieve_approved_hr_policy" in content
    assert "create_onboarding_tasks" in content
    assert "## Constraints" in content


def test_compilation_is_deterministic():
    first = compile_skill("employee_onboarding").read_text(
        encoding="utf-8"
    )
    second = compile_skill("employee_onboarding").read_text(
        encoding="utf-8"
    )

    assert first == second


def test_render_includes_frontmatter_and_steps():
    skill = load_skill_definition("employee_onboarding")
    content = render_skill_markdown(skill)

    assert content.startswith("---\n")
    assert "skill_id: employee_onboarding" in content
    assert "### Step 1: retrieve_hr_policy" in content
    assert "### Step 5: notify_responsible_team" in content


def test_unknown_skill_is_rejected():
    with pytest.raises(FileNotFoundError):
        compile_skill("skill_that_does_not_exist")
