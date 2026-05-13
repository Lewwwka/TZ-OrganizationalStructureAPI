from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.org import Department
from app.repositories.base import BaseRepository


class DepartmentRepository(BaseRepository[Department]):
    def __init__(self, session: AsyncSession):
        super().__init__(Department, session)

    async def name_exists_under_parent(self, name: str, parent_id: int | None) -> bool:
        query = select(Department).where(
            Department.name == name,
            Department.parent_id == parent_id
            if parent_id is not None
            else Department.parent_id.is_(None),
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None

    async def would_create_cycle(self, department_id: int, new_parent_id: int) -> bool:
        """
        Проверяет, является ли new_parent_id потомком department_id.
        Если да, то перемещение создаст цикл.
        """
        visited = {department_id}
        stack = [department_id]
        while stack:
            current = stack.pop()
            children = await self.session.execute(
                select(Department).where(Department.parent_id == current)
            )
            for child in children.scalars():
                if child.id == new_parent_id:
                    return True
                if child.id not in visited:
                    visited.add(child.id)
                    stack.append(child.id)
        return False

    async def get_with_children(
        self, department_id: int, depth: int, include_employees: bool
    ) -> Department | None:
        """
        Возвращает подразделение с загруженными сотрудниками и дочерними подразделениями до указанной глубины.
        """
        stmt = select(Department).where(Department.id == department_id)

        if include_employees:
            stmt = stmt.options(selectinload(Department.employees))

        if depth > 0:
            load_children = selectinload(Department.children)
            current_level = load_children
            for _ in range(depth - 1):
                current_level = current_level.selectinload(Department.children)
            stmt = stmt.options(load_children)

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id_with_employees_and_children(
        self, department_id: int
    ) -> Department | None:
        stmt = (
            select(Department)
            .where(Department.id == department_id)
            .options(
                selectinload(Department.employees), selectinload(Department.children)
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete_cascade(self, dept: Department) -> None:
        """Рекурсивно удаляет подразделение, всех сотрудников и дочерние подразделения."""
        for emp in list(dept.employees):
            await self.session.delete(emp)
        for child in list(dept.children):
            await self.delete_cascade(child)
        await self.session.delete(dept)
        await self.session.flush()

    async def delete_by_id(self, department_id: int) -> None:
        """Прямое удаление подразделения (без ORM)."""
        from sqlalchemy import delete

        stmt = delete(Department).where(Department.id == department_id)
        await self.session.execute(stmt)
        await self.session.flush()
