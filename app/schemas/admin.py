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
    admin_name: str | None
    action_type: str | None
    details: str | None
    created_at: float


class AdminLogsResponse(BaseModel):
    logs: list[ActionLogEntry]
    filter_users: list[str]
    filter_actions: list[str]
