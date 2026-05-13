from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from typing import Optional

from app.schemas.employee import EmployeeOut


class DepartmentBase(BaseModel):
    name: str = Field(min_length=1, max_length=200)


class DepartmentCreate(DepartmentBase):
    parent_id: Optional[int] = None

    @model_validator(mode="after")
    def trim_name(self):
        self.name = self.name.strip()
        return self


class DepartmentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    parent_id: Optional[int] = None

    @model_validator(mode="after")
    def trim_name(self):
        if self.name is not None:
            self.name = self.name.strip()
        return self


class DepartmentOut(BaseModel):
    id: int
    name: str
    parent_id: Optional[int]
    created_at: datetime

    model_config = {"from_attributes": True}


class DepartmentTree(DepartmentOut):
    employees: list["EmployeeOut"] = []
    children: list["DepartmentTree"] = []


DepartmentTree.model_rebuild()
