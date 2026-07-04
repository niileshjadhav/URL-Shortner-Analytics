from sqlalchemy import String, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin
from datetime import datetime, UTC, timezone

class ClickEvent(Base):
    __tablename__ = "click_events"

    id : Mapped[int] = mapped_column(primary_key=True)
    link_id : Mapped[int] = mapped_column(ForeignKey("links.id"))
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    referrer : Mapped[str | None] = mapped_column(String, nullable=True)
    ip: Mapped[str | None] = mapped_column(String, nullable=True)