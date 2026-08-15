from __future__ import annotations
from datetime import datetime
from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_current_user, require_admin
from app.db.database import get_db
from app.repositories.attendance_repo import AttendanceRepository
from app.repositories.override_repo import OverrideRepository
from app.schemas.attendance import AttendanceUpdateRequest, LessonDetailsResponse
from app.services.audit_service import log_action
from app.services.schedule_service import (
    compute_active_times,
    get_base_times_for_date,
)
from app.services.user_service import UserContext, get_all_students_with_tg, get_display_name, get_name_by_student_id
from app.websocket.manager import manager

router = APIRouter(tags=["attendance"])


@router.get("/lesson_details", response_model=LessonDetailsResponse)
async def get_lesson_details(
    date: str,
    time: str,
    user: UserContext = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    att_repo = AttendanceRepository(db)
    ovr_repo = OverrideRepository(db)

    current_att = {r.student_id: r for r in await att_repo.get_for_lesson(date, time)}
    all_day_att = await att_repo.get_for_date(date)

    overrides = await ovr_repo.get_for_date(date)
    base_times = get_base_times_for_date(date)
    active_times = compute_active_times(base_times, overrides)

    student_day_map: dict[int, dict[str, int]] = {}
    for r in all_day_att:
        if r.student_id not in student_day_map:
            student_day_map[r.student_id] = {}
        student_day_map[r.student_id][r.time] = r.status

    students = get_all_students_with_tg()
    result = []
    for s in students:
        s_id = s["id"]
        curr = current_att.get(s_id)
        curr_status = curr.status if curr else 0
        curr_reason = curr.reason if curr else ""

        is_all_day = False
        if curr_status > 0 and active_times:
            marks = student_day_map.get(s_id, {})
            matches = sum(1 for t in active_times if marks.get(t, 0) == curr_status)
            is_all_day = matches == len(active_times)

        result.append({
            "id": s_id,
            "tg_id": s["tg_id"],
            "name": s["name"],
            "status": curr_status,
            "reason": curr_reason,
            "is_all_day": is_all_day,
        })

    return LessonDetailsResponse(students=result)


@router.post("/attendance")
async def update_attendance(
    data: AttendanceUpdateRequest,
    background_tasks: BackgroundTasks,
    user: UserContext = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    att_repo = AttendanceRepository(db)
    ovr_repo = OverrideRepository(db)

    await att_repo.upsert(
        date=data.date,
        time=data.time,
        student_id=data.student_id,
        status=data.status,
        reason=data.reason or "",
    )

    lesson_name = "Пара"
    overrides = await ovr_repo.get_for_date(data.date)
    ovr_map = {o.time: o for o in overrides}
    if data.time in ovr_map and ovr_map[data.time].new_name:
        lesson_name = ovr_map[data.time].new_name
    else:
        weekday = datetime.strptime(data.date, "%Y-%m-%d").weekday()
        from app.data.schedule_data import BASE_SCHEDULE
        found = next(
            (l["name"] for l in BASE_SCHEDULE
             if l["day"] == weekday and l["time"] == data.time
             and l["start"] <= data.date <= l["end"]),
            None,
        )
        if found:
            lesson_name = found

    await db.commit()

    await manager.broadcast({
        "type": "update_attendance",
        "date": data.date,
        "time": data.time,
        "student_id": data.student_id,
        "status": data.status,
        "reason": data.reason,
    })

    admin_name = get_display_name(user)
    stat_str = "Н" if data.status == 1 else "У" if data.status == 2 else "Присутствует"
    student_name = get_name_by_student_id(data.student_id)
    fmt_date = datetime.strptime(data.date, "%Y-%m-%d").strftime("%d.%m")
    log_details = f"{fmt_date} | {data.time} | {lesson_name}\n{student_name} ➔ {stat_str}"

    background_tasks.add_task(log_action, db, admin_name, "Изменение отметки", log_details, user_id=user.id)
    return {"status": "ok"}


@router.post("/attendance/day")
async def update_attendance_day(
    data: AttendanceUpdateRequest,
    background_tasks: BackgroundTasks,
    user: UserContext = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    att_repo = AttendanceRepository(db)
    ovr_repo = OverrideRepository(db)

    overrides = await ovr_repo.get_for_date(data.date)
    base_times = get_base_times_for_date(data.date)
    active_times = compute_active_times(base_times, overrides)

    for t in active_times:
        await att_repo.upsert(
            date=data.date,
            time=t,
            student_id=data.student_id,
            status=data.status,
            reason=data.reason or "",
        )

    await db.commit()

    await manager.broadcast({
        "type": "update_day",
        "date": data.date,
        "student_id": data.student_id,
    })

    admin_name = get_display_name(user)
    student_name = get_name_by_student_id(data.student_id)
    stat_str = "Н" if data.status == 1 else "У" if data.status == 2 else "Присутствует"
    background_tasks.add_task(
        log_action, db, admin_name, "Отметка на весь день",
        f"Студент {student_name} ({data.date}) → {stat_str}",
        user_id=user.id,
    )
    return {"status": "ok"}
