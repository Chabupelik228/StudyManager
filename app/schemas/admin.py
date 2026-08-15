from typing import Optional
from pydantic import BaseModel

class AdminUserRow(BaseModel):
    id: int
    name: str
    is_online: bool
    last_seen: float

class AdminUsersResponse(BaseModel):
    admins: list[AdminUserRow]

class ActionLogEntry(BaseModel):
    id: int
    admin_name: Optional[str]
    action_type: Optional[str]
    details: Optional[str]
    created_at: float

class AdminLogsResponse(BaseModel):
    logs: list[ActionLogEntry]
    filter_users: list[str]
    filter_actions: list[str]


