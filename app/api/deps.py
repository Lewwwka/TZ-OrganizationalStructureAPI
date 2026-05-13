from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.repositories.department import DepartmentRepository
from app.repositories.employee import EmployeeRepository
from app.services.department import DepartmentService
from app.services.employee import EmployeeService


def get_department_repo(
    session: AsyncSession = Depends(get_db),
) -> DepartmentRepository:
    return DepartmentRepository(session)


def get_employee_repo(session: AsyncSession = Depends(get_db)) -> EmployeeRepository:
    return EmployeeRepository(session)


def get_department_service(
    repo: DepartmentRepository = Depends(get_department_repo),
) -> DepartmentService:
    return DepartmentService(repo)


def get_employee_service(
    emp_repo: EmployeeRepository = Depends(get_employee_repo),
    dept_repo: DepartmentRepository = Depends(get_department_repo),
) -> EmployeeService:
    return EmployeeService(emp_repo, dept_repo)
