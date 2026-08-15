from typing import Optional
from pydantic import BaseModel

class DutyAssignRequest(BaseModel):
    date: str
    student_ids: list[int]

class DutyStudentRow(BaseModel):
    id: int
    name: str
    tg_id: int
    date: Optional[str] = None
    is_absent_now: bool

class DutiesResponse(BaseModel):
    duties: list[DutyStudentRow]
