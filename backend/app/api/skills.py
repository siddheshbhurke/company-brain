
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.skills.skill_registry import discover_skills, get_skill
from app.skills.generic_planner import build_execution_plan
from app.skills.skill_compiler import compile_skill


router = APIRouter(prefix="/api", tags=["Skills"])


class PlanRequest(BaseModel):
    skill_id: str = Field(
        min_length=1,
        description="ID of the skill to plan",
    )
    inputs: dict[str, Any] = Field(default_factory=dict)
    available_tools: list[str] | None = Field(
        default=None,
        description="Tool names available to the planner. Null means unchecked.",
    )


@router.get("/skills")
def list_skills():
    """List all available skill definitions."""
    try:
        return {"skills": discover_skills()}
    except (ValueError, OSError) as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to discover skills: {exc}",
        ) from exc


@router.get("/skills/{skill_id}")
def retrieve_skill(skill_id: str):
    """Retrieve a validated skill definition."""
    try:
        return get_skill(skill_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Skill not found.") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/plans")
def create_plan(request: PlanRequest):
    """Create a proposed plan without executing any actions."""
    try:
        return build_execution_plan(
            skill_id=request.skill_id,
            inputs=request.inputs,
            available_tools=(
                set(request.available_tools)
                if request.available_tools is not None
                else None
            ),
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Skill not found.") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/skills/{skill_id}/compile")
def compile_skill_endpoint(skill_id: str):
    """Compile a validated skill into a SKILL.md artifact."""
    try:
        output_path = compile_skill(skill_id)
        return {
            "skill_id": skill_id,
            "status": "compiled",
            "artifact": f"skills/generated/{skill_id}/SKILL.md",
            "message": "SKILL.md generated successfully.",
        }
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Skill not found.") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except OSError as exc:
        raise HTTPException(
            status_code=500,
            detail="Unable to write the skill artifact.",
        ) from exc
