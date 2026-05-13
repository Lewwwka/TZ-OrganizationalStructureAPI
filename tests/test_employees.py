import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_employee_invalid_department(client: AsyncClient):
    resp = await client.post(
        "/api/v1/departments/9999/employees",
        json={"full_name": "Ghost", "position": "Nothing"},
    )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_create_employee_valid(client: AsyncClient):
    dept = await client.post("/api/v1/departments/", json={"name": "HR"})
    resp = await client.post(
        f"/api/v1/departments/{dept.json()['id']}/employees",
        json={
            "full_name": "Alice Smith",
            "position": "Recruiter",
            "hired_at": "2025-01-15",
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["full_name"] == "Alice Smith"
    assert data["department_id"] == dept.json()["id"]


@pytest.mark.asyncio
async def test_create_employee_empty_name(client: AsyncClient):
    dept = await client.post("/api/v1/departments/", json={"name": "Test"})
    resp = await client.post(
        f"/api/v1/departments/{dept.json()['id']}/employees",
        json={"full_name": "", "position": "Dev"},
    )
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_create_employee_long_name(client: AsyncClient):
    dept = await client.post("/api/v1/departments/", json={"name": "Test"})
    resp = await client.post(
        f"/api/v1/departments/{dept.json()['id']}/employees",
        json={"full_name": "A" * 201, "position": "Dev"},
    )
    assert resp.status_code == 422
