from __future__ import annotations

import httpx

from app.core.config import get_settings


async def send_message(
    chat_id: str | int,
    text: str,
    parse_mode: str = "HTML",
    reply_markup: dict | None = None,
) -> dict | None:
    settings = get_settings()
    payload: dict = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode,
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(
                f"https://api.telegram.org/bot{settings.bot_token}/sendMessage",
                json=payload,
                timeout=10,
            )
            return resp.json()
        except Exception as e:
            print(f"[telegram] sendMessage error: {e}")
            return None


async def check_membership(user_id: int) -> str | None:
    settings = get_settings()
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(
                f"https://api.telegram.org/bot{settings.bot_token}/getChatMember",
                params={"chat_id": settings.group_id, "user_id": user_id},
                timeout=10,
            )
            if resp.status_code == 200:
                return resp.json().get("result", {}).get("status")
        except Exception as e:
            print(f"[telegram] getChatMember error: {e}")
    return None
