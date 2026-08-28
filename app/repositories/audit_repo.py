from __future__ import annotations

import time

from sqlalchemy import delete, distinct, select
from sqlalchemy.dialects.postgresql import insert as pg_insert

from app.models.audit import ActionLog, AdminOnline
from app.repositories.base import BaseRepository


class AuditRepository(BaseRepository):
    async def log_action(
        self, admin_name: str, action_type: str, details: str
    ) -> ActionLog:
        now = time.time()
        entry = ActionLog(
            admin_name=admin_name,
            action_type=action_type,
            details=details,
            created_at=now,
        )
        self.session.add(entry)
        await self.session.execute(
            delete(ActionLog).where(ActionLog.created_at < now - 604800)
        )
        return entry

    async def get_action_logs(
        self,
        offset: int = 0,
        limit: int = 20,
        user_filter: str = "all",
        action_filter: str = "all",
    ) -> tuple[list[ActionLog], list[str], list[str]]:
        q = select(ActionLog)
        if user_filter != "all":
            q = q.where(ActionLog.admin_name == user_filter)
        if action_filter != "all":
            q = q.where(ActionLog.action_type == action_filter)
        q = q.order_by(ActionLog.created_at.desc()).offset(offset).limit(limit)

        result = await self.session.execute(q)
        logs = list(result.scalars().all())

        users_r = await self.session.execute(
            select(distinct(ActionLog.admin_name)).order_by(ActionLog.admin_name)
        )
        actions_r = await self.session.execute(
            select(distinct(ActionLog.action_type)).order_by(ActionLog.action_type)
        )
        users = [r for (r,) in users_r.all() if r]
        actions = [r for (r,) in actions_r.all() if r]
        return logs, users, actions

    async def delete_action_log(self, log_id: int) -> None:
        result = await self.session.execute(
            select(ActionLog).where(ActionLog.id == log_id)
        )
        log = result.scalar_one_or_none()
        if log:
            await self.session.delete(log)

    async def upsert_admin_online(self, user_id: int, name: str) -> None:
        stmt = pg_insert(AdminOnline).values(
            user_id=user_id, name=name, last_seen=time.time()
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=["user_id"],
            set_={"name": stmt.excluded.name, "last_seen": stmt.excluded.last_seen},
        )
        await self.session.execute(stmt)

    async def get_all_admins_online(self) -> dict[int, AdminOnline]:
        result = await self.session.execute(select(AdminOnline))
        return {row.user_id: row for row in result.scalars().all()}
