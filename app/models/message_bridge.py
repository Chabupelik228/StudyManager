from sqlalchemy import BigInteger, Double
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class MessageBridge(Base):
    __tablename__ = "message_bridge"

    tg_msg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    vk_msg_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    created_at: Mapped[float | None] = mapped_column(Double, nullable=True)
