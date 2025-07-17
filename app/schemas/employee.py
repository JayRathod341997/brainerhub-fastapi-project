from pydantic import BaseModel
from typing import Optional

class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    salary: float
    manager_id: Optional[int] = None
    department_id: int
    company_name: str  # Add company_name field

class EmployeeCreate(EmployeeBase):
    company_id: int = 0  # Will be set during processing

class Employee(EmployeeBase):
    id: int
    company_id: int  # Actual company ID from database

    class Config:
        orm_mode = True