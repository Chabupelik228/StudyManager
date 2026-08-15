from __future__ import annotations
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.override import Override
from app.repositories.base import BaseRepository

class OverrideRepository(BaseRepository):
    async def get_for_date(self, date: str) -> list[Override]:
        result = await self.session.execute(
            select(Override).where(Override.date == date)
        )
        return list(result.scalars().all())

    async def get_all(self) -> list[Override]:
        result = await self.session.execute(select(Override))
        return list(result.scalars().all())

    async def upsert(
        self,
        date: str,
        time: str,
        new_name: str | None,
        new_teacher: str | None,
        is_canceled: int,
    ) -> None:
        stmt = pg_insert(Override).values(
            date=date,
            time=time,
            new_name=new_name,
            new_teacher=new_teacher,
            is_canceled=is_canceled,
        )
        stmt = stmt.on_conflict_do_update(
            constraint="uq_override",
            set_={
                "new_name": stmt.excluded.new_name,
                "new_teacher": stmt.excluded.new_teacher,
                "is_canceled": stmt.excluded.is_canceled,
            },
        )
        await self.session.execute(stmt)
