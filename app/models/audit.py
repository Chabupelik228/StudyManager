from sqlalchemy import BigInteger, Double, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class ActionLog(Base):
    __tablename__ = "action_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    admin_name: Mapped[str | None] = mapped_column(
        String(255), nullable=True, index=True
    )
    action_type: Mapped[str | None] = mapped_column(
        String(255), nullable=True, index=True
    )
    details: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[float] = mapped_column(Double, nullable=False, index=True)


class AdminOnline(Base):
    __tablename__ = "admins_online"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    last_seen: Mapped[float] = mapped_column(Double, nullable=False)
