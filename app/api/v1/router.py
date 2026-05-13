from fastapi import APIRouter
from app.api.v1 import departments, employees

router = APIRouter(prefix="/api/v1")
router.include_router(departments.router)
router.include_router(employees.router)
