from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.audit_repo import AuditRepository
from app.websocket.manager import manager


async def log_action(
    session: AsyncSession,
    admin_name: str,
    action_type: str,
    details: str,
) -> None:
    repo = AuditRepository(session)
    entry = await repo.log_action(admin_name, action_type, details)
    await session.commit()

    await manager.broadcast({
        "type": "new_log",
        "entry": {
            "admin_name": entry.admin_name,
            "action_type": entry.action_type,
            "details": entry.details,
            "created_at": entry.created_at,
        },
    })

