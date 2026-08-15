from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class Duty(Base):
    __tablename__ = "duties"

    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("students.id", ondelete="CASCADE"), primary_key=True)
    date: Mapped[str | None] = mapped_column(String(10), nullable=True)

class WebUndo(Base):
    __tablename__ = "web_undos"

    undo_id: Mapped[str] = mapped_column(String(8), primary_key=True)
    data: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[float] = mapped_column(nullable=False)
