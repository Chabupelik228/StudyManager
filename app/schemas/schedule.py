from typing import Optional
from pydantic import BaseModel

class LessonResponse(BaseModel):
    time: str
    name: str
    teacher: str
    canceled: bool
    absent_count: int
    is_current: bool

class ScheduleResponse(BaseModel):
    date: str
    lessons: list[LessonResponse]

class OverrideUpdateRequest(BaseModel):
    date: str
    time: str
    new_name: Optional[str] = None
    new_teacher: Optional[str] = None
    is_canceled: int
