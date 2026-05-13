from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional


class EmployeeBase(BaseModel):
    full_name: str = Field(min_length=1, max_length=200)
    position: str = Field(min_length=1, max_length=200)
    hired_at: Optional[date] = None


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeOut(EmployeeBase):
    id: int
    department_id: int
    created_at: datetime

    model_config = {"from_attributes": True}
