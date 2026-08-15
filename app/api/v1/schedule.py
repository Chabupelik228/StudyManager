from __future__ import annotations
from datetime import datetime
from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_current_user, require_admin, get_request_details
from app.db.database import get_db
from app.repositories.attendance_repo import AttendanceRepository
from app.repositories.override_repo import OverrideRepository
from app.schemas.schedule import OverrideUpdateRequest, ScheduleResponse
from app.services.audit_service import log_action
from app.services.schedule_service import MSK, build_schedule
from app.services.user_service import UserContext, get_display_name
from app.websocket.manager import manager

router = APIRouter(tags=["schedule"])


@router.get("/schedule", response_model=ScheduleResponse)
async def get_schedule(
    date: str,
    user: UserContext = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    now = datetime.now(MSK)
    current_date_str = now.strftime("%Y-%m-%d")
    current_time_str = now.strftime("%H:%M") if date == current_date_str else None

    att_repo = AttendanceRepository(db)
    ovr_repo = OverrideRepository(db)

    overrides = await ovr_repo.get_for_date(date)
    absent_counts = await att_repo.get_absent_count_by_time(date)

    lessons = build_schedule(date, overrides, absent_counts, current_time_str)
    return ScheduleResponse(date=date, lessons=lessons)


@router.post("/override")
async def update_override(
    data: OverrideUpdateRequest,
    background_tasks: BackgroundTasks,
    user: UserContext = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
    req: dict = Depends(get_request_details),
):
    att_repo = AttendanceRepository(db)
    ovr_repo = OverrideRepository(db)

    await ovr_repo.upsert(
        date=data.date,
        time=data.time,
        new_name=data.new_name,
        new_teacher=data.new_teacher,
        is_canceled=data.is_canceled,
    )

    if data.is_canceled == 1:
        await att_repo.delete_for_lesson(data.date, data.time)

    await db.commit()
    await manager.broadcast({"type": "override", "date": data.date})

    admin_name = get_display_name(user)
    action = "Отмена пары" if data.is_canceled else "Замена пары"
    background_tasks.add_task(
        log_action, db, admin_name, action,
        f"{data.date} {data.time} → {data.new_name}",
        user_id=user.id,
    )

    return {"status": "ok"}
