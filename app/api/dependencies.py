from __future__ import annotations

import time

from fastapi import Depends, Header, HTTPException, Request

from app.core.config import get_settings
from app.core.security import decode_access_token, validate_tg_init_data
from app.services.user_service import UserContext

_CACHE_TTL = 3600
_AUTH_DATE_MAX_AGE = 86400  # 24 hours — Telegram recommendation

# Pre-warm membership cache with trusted user IDs from config at startup
_membership_cache: dict[int, tuple[float, bool]] = {}


async def get_current_user(
    request: Request,
    x_tg_data: str | None = Header(None, alias="X-Telegram-Init-Data"),
    authorization: str | None = Header(None),
) -> UserContext:
    if x_tg_data:
        user_dict = validate_tg_init_data(x_tg_data)
        if user_dict and user_dict.get("id"):
            # Check that initData is fresh (max 24h per Telegram recommendation)
            auth_date = user_dict.get("auth_date")
            if auth_date:
                try:
                    age = time.time() - int(auth_date)
                    if age > _AUTH_DATE_MAX_AGE:
                        raise HTTPException(
                            status_code=401, detail="Telegram initData expired"
                        )
                except (ValueError, TypeError):
                    pass  # non-critical if auth_date is malformed
            return UserContext(
                id=int(user_dict["id"]),
                first_name=user_dict.get("first_name", ""),
                username=user_dict.get("username"),
            )
        raise HTTPException(status_code=401, detail="Invalid Telegram initData")

    if authorization and authorization.startswith("Bearer "):
        token = authorization.removeprefix("Bearer ").strip()
        payload = decode_access_token(token)
        if payload and (sub := payload.get("sub")):
            try:
                return UserContext(id=int(sub))
            except ValueError:
                pass
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    raise HTTPException(status_code=401, detail="Authentication required")


async def require_admin(user: UserContext = Depends(get_current_user)) -> UserContext:
    settings = get_settings()
    if user.id not in settings.admin_ids_list and user.id != settings.developer_id:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


async def require_developer(
    user: UserContext = Depends(get_current_user),
) -> UserContext:
    if not user.is_developer:
        raise HTTPException(status_code=403, detail="Developer only")
    return user


async def get_request_details(request: Request) -> dict:
    ip = request.headers.get("x-forwarded-for")
    if ip:
        ip = ip.split(",")[0].strip()
    else:
        ip = request.client.host if request.client else "Unknown"
    return {
        "ip": ip,
        "user_agent": request.headers.get("user-agent", "N/A"),
    }
