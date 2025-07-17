from pydantic import BaseModel

class ImportResult(BaseModel):
    filename: str
    employee_count: int
    status: str