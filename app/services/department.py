from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.repositories.department import DepartmentRepository
from app.models.org import Department
from app.schemas.department import DepartmentCreate, DepartmentUpdate, DepartmentTree
from app.schemas.employee import EmployeeOut


class DepartmentService:
    def __init__(self, repo: DepartmentRepository):
        self.repo = repo

    async def create(self, data: DepartmentCreate) -> Department:
        data.name = data.name.strip()
        if data.parent_id is not None:
            parent = await self.repo.get_by_id(data.parent_id)
            if not parent:
                raise HTTPException(
                    status_code=404, detail="Parent department not found"
                )

        if await self.repo.name_exists_under_parent(data.name, data.parent_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Department with this name already exists under the same parent",
            )

        dept = Department(**data.model_dump())
        return await self.repo.add(dept)

    async def update(self, id: int, data: DepartmentUpdate) -> Department:
        dept = await self.repo.get_by_id(id)
        if not dept:
            raise HTTPException(status_code=404, detail="Department not found")

        if data.name is not None:
            new_name = data.name.strip()
            if new_name != dept.name:
                if await self.repo.name_exists_under_parent(new_name, dept.parent_id):
                    raise HTTPException(
                        status_code=409, detail="Department name already exists"
                    )
                dept.name = new_name

        if data.parent_id is not None:
            if data.parent_id == id:
                raise HTTPException(
                    status_code=400, detail="Department cannot be its own parent"
                )
            if await self.repo.would_create_cycle(id, data.parent_id):
                raise HTTPException(
                    status_code=409, detail="Moving would create a cycle"
                )
            new_parent = await self.repo.get_by_id(data.parent_id)
            if not new_parent:
                raise HTTPException(
                    status_code=404, detail="New parent department not found"
                )
            dept.parent_id = data.parent_id

        await self.repo.session.flush()
        return dept

    async def delete(self, id: int, mode: str, reassign_to: int | None = None):
        if mode == "cascade":
            dept = await self.repo.get_by_id_with_employees_and_children(id)
            if not dept:
                raise HTTPException(status_code=404, detail="Department not found")
            await self.repo.delete_cascade(dept)

        elif mode == "reassign":
            if reassign_to is None:
                raise HTTPException(
                    status_code=400, detail="reassign_to_department_id required"
                )
            dept = await self.repo.get_by_id_with_employees_and_children(id)
            if not dept:
                raise HTTPException(status_code=404, detail="Department not found")
            target_dept = await self.repo.get_by_id(reassign_to)
            if not target_dept:
                raise HTTPException(
                    status_code=404, detail="Target department not found"
                )

            for emp in list(dept.employees):
                emp.department_id = reassign_to

            for child in list(dept.children):
                child.parent_id = reassign_to

            await self.repo.session.flush()

            await self.repo.delete_by_id(id)

        else:
            raise HTTPException(status_code=400, detail="Invalid mode")

    async def get_tree(
        self, id: int, depth: int, include_employees: bool
    ) -> DepartmentTree:
        dept = await self.repo.get_with_children(id, depth, include_employees)
        if not dept:
            raise HTTPException(status_code=404, detail="Department not found")
        return await self._build_tree(
            dept, include_employees, current_depth=1, max_depth=depth
        )

    async def _build_tree(
        self,
        dept: Department,
        include_employees: bool,
        current_depth: int,
        max_depth: int,
    ) -> DepartmentTree:
        children = []
        if current_depth < max_depth:
            for child in dept.children:
                children.append(
                    await self._build_tree(
                        child, include_employees, current_depth + 1, max_depth
                    )
                )

        employees = []
        if include_employees:
            sorted_employees = sorted(dept.employees, key=lambda e: e.created_at)
            employees = [EmployeeOut.model_validate(e) for e in sorted_employees]

        return DepartmentTree(
            id=dept.id,
            name=dept.name,
            parent_id=dept.parent_id,
            created_at=dept.created_at,
            employees=employees,
            children=children,
        )

    async def get_by_id_with_employees(self, department_id: int) -> Department | None:
        stmt = (
            select(Department)
            .where(Department.id == department_id)
            .options(selectinload(Department.employees))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
