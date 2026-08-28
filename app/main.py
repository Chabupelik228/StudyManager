from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, Response

from app.api.v1 import admin, attendance, auth, duties, schedule, stats
from app.core.config import get_settings
from app.core.security import validate_tg_init_data
from app.db.database import async_session_maker, engine
from app.services.audit_service import log_action
from app.services.user_service import UserContext, get_display_name, load_student_cache
from app.websocket.manager import manager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("▶ Starting StudyManager...")
    try:
        async with engine.begin() as conn:
            from app.models.base import Base

            await conn.run_sync(Base.metadata.create_all)
        logger.info("✅ Database tables initialized")
    except Exception as e:
        logger.error(f"❌ Database initialization error: {e}")
        raise

    async with async_session_maker() as session:
        await load_student_cache(session)
    logger.info("✅ Student cache loaded")

    logger.info("🚀 StudyManager is ready")
    yield

    await engine.dispose()
    logger.info("🛑 StudyManager stopped")


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="StudyManager API",
        version="2.0.0",
        docs_url="/docs" if settings.show_docs else None,
        redoc_url="/redoc" if settings.show_docs else None,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    PREFIX = "/api"
    app.include_router(auth.router, prefix=PREFIX)
    app.include_router(schedule.router, prefix=PREFIX)
    app.include_router(attendance.router, prefix=PREFIX)
    app.include_router(duties.router, prefix=PREFIX)
    app.include_router(stats.router, prefix=PREFIX)
    app.include_router(admin.router, prefix=PREFIX)

    @app.get("/api/uploads/{filename}")
    async def get_upload(filename: str):
        path = f"data/uploads/{filename}"
        if os.path.exists(path):
            headers = {"Cache-Control": "public, max-age=31536000"}
            return FileResponse(path, headers=headers)
        return Response(status_code=404)

    @app.get("/api/avatar/{tg_id}")
    async def get_avatar(tg_id: int):
        path = f"data/avatars/{tg_id}.jpg"
        if os.path.exists(path):
            return FileResponse(path, media_type="image/jpeg")
        return Response(status_code=404)

    @app.get("/api/ping")
    async def ping_health():
        return {"status": "ok"}

    @app.post("/internal/broadcast_duties")
    @app.post("/api/internal/broadcast_duties")
    async def internal_broadcast_duties(
        x_internal_secret: str | None = None,
        request: Request | None = None
    ):
        settings = get_settings()
        # Require a shared secret from the bot to prevent public abuse
        secret = request.headers.get("X-Internal-Secret", "") if request else ""
        if settings.internal_secret and secret != settings.internal_secret:
            return JSONResponse({"error": "Forbidden"}, status_code=403)
        await manager.broadcast({"type": "update_duties"})
        return {"status": "ok"}

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        ip = websocket.headers.get("x-forwarded-for", "")
        if ip:
            ip = ip.split(",")[0].strip()
        else:
            ip = websocket.client.host if websocket.client else "Unknown"
        user_agent = websocket.headers.get("user-agent", "N/A")

        await manager.connect(websocket)
        try:
            auth_data = await websocket.receive_text()
            tg_user = validate_tg_init_data(auth_data)

            if not tg_user:
                async with async_session_maker() as session:
                    await log_action(
                        session,
                        "System",
                        "WS Auth Failed",
                        f"IP: {ip}, Agent: {user_agent}",
                    )
                await websocket.close(code=1008)
                return

            user_id = int(tg_user["id"])
            ctx = UserContext(
                id=user_id,
                first_name=tg_user.get("first_name", ""),
            )
            user_name = get_display_name(ctx)

            async with async_session_maker() as session:
                await log_action(
                    session, user_name, "WS Connected", f"IP: {ip}, Agent: {user_agent}"
                )

            while True:
                await websocket.receive_text()

        except WebSocketDisconnect:
            manager.disconnect(websocket)
        except Exception:
            manager.disconnect(websocket)

    return app


app = create_app()
