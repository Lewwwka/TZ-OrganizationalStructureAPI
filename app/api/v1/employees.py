from fastapi import APIRouter, Depends
from app.api.deps import get_employee_service
from app.schemas.employee import EmployeeCreate, EmployeeOut
from app.services.employee import EmployeeService

router = APIRouter(prefix="/departments", tags=["employees"])


@router.post("/{department_id}/employees", response_model=EmployeeOut, status_code=201)
async def create_employee(
    department_id: int,
    data: EmployeeCreate,
    service: EmployeeService = Depends(get_employee_service),
):
    return await service.create(department_id, data)
