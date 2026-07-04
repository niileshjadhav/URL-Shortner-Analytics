from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.models.click_event import ClickEvent


async def record_click(db: AsyncSession, link_id: int, ip: str | None = None, referrer: str | None = None):
    event = ClickEvent(link_id=link_id, ip=ip, referrer=referrer)
    db.add(event)
    await db.commit()


async def get_total_clicks(db: AsyncSession, link_id: int) -> int:
    result = await db.execute(
        select(func.count()).select_from(ClickEvent).where(ClickEvent.link_id == link_id)
    )
    return result.scalar_one()