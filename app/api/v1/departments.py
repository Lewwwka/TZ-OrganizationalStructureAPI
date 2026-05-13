from fastapi import APIRouter, Depends, Query
from app.api.deps import get_department_service
from app.schemas.department import (
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentOut,
    DepartmentTree,
)
from app.services.department import DepartmentService

router = APIRouter(prefix="/departments", tags=["departments"])


@router.post("/", response_model=DepartmentOut, status_code=201)
async def create_department(
    data: DepartmentCreate,
    service: DepartmentService = Depends(get_department_service),
):
    return await service.create(data)


@router.get("/{id}", response_model=DepartmentTree)
async def get_department(
    id: int,
    depth: int = Query(1, ge=1, le=5, description="Глубина вложенности подразделений"),
    include_employees: bool = Query(True, description="Включать сотрудников в ответ"),
    service: DepartmentService = Depends(get_department_service),
):
    return await service.get_tree(id, depth, include_employees)


@router.patch("/{id}", response_model=DepartmentOut)
async def update_department(
    id: int,
    data: DepartmentUpdate,
    service: DepartmentService = Depends(get_department_service),
):
    return await service.update(id, data)


@router.delete("/{id}", status_code=204)
async def delete_department(
    id: int,
    mode: str = Query(..., description="cascade или reassign"),
    reassign_to_department_id: int | None = Query(None),
    service: DepartmentService = Depends(get_department_service),
):
    await service.delete(id, mode, reassign_to_department_id)
    return None
