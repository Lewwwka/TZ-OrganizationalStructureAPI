import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_department(client: AsyncClient):
    payload = {"name": "Engineering", "parent_id": None}
    resp = await client.post("/api/v1/departments/", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Engineering"
    assert data["parent_id"] is None
    assert "id" in data


@pytest.mark.asyncio
async def test_create_duplicate_name_same_parent(client: AsyncClient):
    await client.post("/api/v1/departments/", json={"name": "QA"})
    resp = await client.post("/api/v1/departments/", json={"name": "QA"})
    assert resp.status_code == 409
    assert "already exists" in resp.json()["detail"]


@pytest.mark.asyncio
async def test_get_department_with_employees(client: AsyncClient):
    dept = await client.post("/api/v1/departments/", json={"name": "R&D"})
    dept_id = dept.json()["id"]
    await client.post(
        f"/api/v1/departments/{dept_id}/employees",
        json={"full_name": "John Doe", "position": "Developer"},
    )
    resp = await client.get(f"/api/v1/departments/{dept_id}?include_employees=true")
    assert resp.status_code == 200
    tree = resp.json()
    assert len(tree["employees"]) == 1
    assert tree["employees"][0]["full_name"] == "John Doe"


@pytest.mark.asyncio
async def test_delete_cascade(client: AsyncClient):
    dept = await client.post("/api/v1/departments/", json={"name": "ToDelete"})
    dept_id = dept.json()["id"]
    await client.post(
        f"/api/v1/departments/{dept_id}/employees",
        json={"full_name": "Tmp", "position": "Tmp"},
    )
    resp = await client.delete(f"/api/v1/departments/{dept_id}?mode=cascade")
    assert resp.status_code == 204
    resp = await client.get(f"/api/v1/departments/{dept_id}")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_reassign(client: AsyncClient):
    src = await client.post("/api/v1/departments/", json={"name": "Src"})
    tgt = await client.post("/api/v1/departments/", json={"name": "Tgt"})
    src_id = src.json()["id"]
    tgt_id = tgt.json()["id"]

    await client.post(
        f"/api/v1/departments/{src_id}/employees",
        json={"full_name": "Move Me", "position": "Tester"},
    )
    resp = await client.delete(
        f"/api/v1/departments/{src_id}?mode=reassign&reassign_to_department_id={tgt_id}"
    )
    assert resp.status_code == 204

    tgt_resp = await client.get(f"/api/v1/departments/{tgt_id}?include_employees=true")
    emps = tgt_resp.json()["employees"]
    assert len(emps) == 1
    assert emps[0]["full_name"] == "Move Me"
    assert (await client.get(f"/api/v1/departments/{src_id}")).status_code == 404


@pytest.mark.asyncio
async def test_move_department_cycle_prevention(client: AsyncClient):
    root = await client.post("/api/v1/departments/", json={"name": "Root"})
    child = await client.post(
        "/api/v1/departments/", json={"name": "Child", "parent_id": root.json()["id"]}
    )
    resp = await client.patch(
        f"/api/v1/departments/{root.json()['id']}",
        json={"parent_id": child.json()["id"]},
    )
    assert resp.status_code == 409


@pytest.mark.asyncio
async def test_update_self_parent(client: AsyncClient):
    dept = await client.post("/api/v1/departments/", json={"name": "Dept"})
    dept_id = dept.json()["id"]
    resp = await client.patch(
        f"/api/v1/departments/{dept_id}", json={"parent_id": dept_id}
    )
    assert resp.status_code == 400
    assert "cannot be its own parent" in resp.json()["detail"]
