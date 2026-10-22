
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_list_skills():
    response = client.get("/api/skills")

    assert response.status_code == 200

    skill_ids = {
        skill["skill_id"]
        for skill in response.json()["skills"]
    }

    assert "process_refund" in skill_ids
    assert "employee_onboarding" in skill_ids


def test_retrieve_employee_onboarding_skill():
    response = client.get("/api/skills/employee_onboarding")

    assert response.status_code == 200
    assert response.json()["name"] == "Employee Onboarding"


def test_unknown_skill_returns_404():
    response = client.get("/api/skills/not_a_real_skill")

    assert response.status_code == 404


def test_create_plan_with_missing_inputs():
    response = client.post(
        "/api/plans",
        json={"skill_id": "employee_onboarding"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "blocked_missing_inputs"
    assert response.json()["execution_started"] is False


def test_create_plan_with_missing_tools():
    response = client.post(
        "/api/plans",
        json={
            "skill_id": "employee_onboarding",
            "inputs": {
                "employee_id": "EMP-TEST",
                "start_date": "2026-11-01",
                "department": "Engineering",
            },
            "available_tools": [],
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "blocked_missing_tools"


def test_compile_skill():
    response = client.post(
        "/api/skills/employee_onboarding/compile"
    )

    assert response.status_code == 200
    assert response.json()["status"] == "compiled"
    assert response.json()["artifact"].endswith("SKILL.md")


def test_root_and_health_endpoints_still_work():
    assert client.get("/").status_code == 200
    assert client.get("/health").json()["status"] == "healthy"
