from fastapi import HTTPException
from app.repositories.employee import EmployeeRepository
from app.repositories.department import DepartmentRepository
from app.models.org import Employee
from app.schemas.employee import EmployeeCreate


class EmployeeService:
    def __init__(self, emp_repo: EmployeeRepository, dept_repo: DepartmentRepository):
        self.emp_repo = emp_repo
        self.dept_repo = dept_repo

    async def create(self, department_id: int, data: EmployeeCreate) -> Employee:
        data.full_name = data.full_name.strip()
        data.position = data.position.strip()

        dept = await self.dept_repo.get_by_id(department_id)
        if not dept:
            raise HTTPException(status_code=404, detail="Department not found")

        employee = Employee(
            department_id=department_id,
            full_name=data.full_name,
            position=data.position,
            hired_at=data.hired_at,
        )
        return await self.emp_repo.add(employee)
