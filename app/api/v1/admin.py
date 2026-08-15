from __future__ import annotations
import time
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_current_user, require_admin, require_developer
from app.core.config import get_settings
from app.db.database import get_db
from app.repositories.audit_repo import AuditRepository
from app.services.user_service import UserContext, get_display_name
from app.websocket.manager import manager

router = APIRouter(tags=["admin"])


@router.get("/admin/ping")
@router.get("/ping_admin")
async def ping(
    user: UserContext = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    settings = get_settings()
    if user.is_developer:
        return {"status": "ok"}

    if user.id in settings.admin_ids_list:
        name = get_display_name(user)
        repo = AuditRepository(db)
        await repo.upsert_admin_online(user.id, name)
        await db.commit()

        await manager.broadcast({
            "type": "admin_status",
            "user_id": user.id,
            "last_seen": time.time(),
        })

    return {"status": "ok"}


@router.get("/admin/users")
@router.get("/admin_users")
async def get_admin_users(
    user: UserContext = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    settings = get_settings()
    repo = AuditRepository(db)
    online_data = await repo.get_all_admins_online()

    now = time.time()
    admins_list = []
    for admin_id in settings.admin_ids_list:
        data = online_data.get(admin_id)
        name = "ID " + str(admin_id)
        if data:
            name = data.name
        elif admin_id == settings.curator_id:
            name = "Виктория Александровна"
        else:
            from app.services.user_service import _tg_id_to_name
            name = _tg_id_to_name.get(admin_id, name)

        last_seen = data.last_seen if data else 0

        if admin_id == settings.developer_id:
            is_online = False
            last_seen = 0
        else:
            is_online = (now - last_seen) < 65

        admins_list.append({
            "id": admin_id,
            "name": name,
            "is_online": is_online,
            "last_seen": last_seen,
        })

    admins_list.sort(key=lambda x: x["is_online"], reverse=True)
    return {"admins": admins_list}


@router.get("/init")
@router.get("/admin/init")
async def get_init(user: UserContext = Depends(get_current_user)):
    settings = get_settings()
    return {
        "role": "admin" if (user.id in settings.admin_ids_list or user.id == settings.developer_id) else "viewer",
        "user": {"id": user.id, "first_name": user.first_name},
    }


@router.get("/admin/logs")
@router.get("/logs")
async def get_admin_logs(
    offset: int = 0,
    limit: int = 20,
    user_filter: str = "all",
    action_filter: str = "all",
    user: UserContext = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    repo = AuditRepository(db)
    logs, users, actions = await repo.get_action_logs(offset, limit, user_filter, action_filter)
    return {
        "logs": [
            {
                "id": l.id,
                "admin_name": l.admin_name,
                "action_type": l.action_type,
                "details": l.details,
                "created_at": l.created_at,
            }
            for l in logs
        ],
        "filter_users": users,
        "filter_actions": actions,
    }


@router.delete("/admin/logs/{log_id}")
@router.delete("/logs/{log_id}")
async def delete_log(
    log_id: int,
    user: UserContext = Depends(require_developer),
    db: AsyncSession = Depends(get_db),
):
    repo = AuditRepository(db)
    await repo.delete_action_log(log_id)
    await db.commit()
    return {"status": "ok"}
