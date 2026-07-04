from sqlalchemy import String, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.api.db.base import Base, TimestampMixin
import datetime

class Link(Base, TimestampMixin):
    __tablename__ = "links"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)
    target_url : Mapped[str] = mapped_column(String, nullable=False)
    is_active : Mapped[bool] = mapped_column(Boolean, default=True)
    expires_at : Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    owner : Mapped[str | None] = mapped_column(String, nullable=True)