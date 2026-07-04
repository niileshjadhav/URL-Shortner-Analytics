from sqlalchemy import String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.api.db.base import Base, TimestampMixin
from datetime import datetime, UTC

class ClickEvent(Base):
    __tablename__ = "click_events"

    id : Mapped[int] = mapped_column(primary_key=True)
    link_id : Mapped[int] = mapped_column(ForeignKey("links.id"))
    timestamp : Mapped[datetime] = mapped_column(default=datetime.now(UTC))
    referrer : Mapped[str | None] = mapped_column(String, nullable=True)
    ip: Mapped[str | None] = mapped_column(String, nullable=True)