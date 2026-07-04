from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.click_event import ClickEvent


async def record_click(db: AsyncSession, link_id: int, ip: str | None = None, referrer: str | None = None):
    event = ClickEvent(link_id=link_id, ip=ip, referrer=referrer)
    print(f"Recording click event: link_id={link_id}, ip={ip}, referrer={referrer}")
    db.add(event)
    print(f"Click event added to session: {event}")
    await db.commit()
    print(f"Click event committed to database: {event}")


async def get_total_clicks(db: AsyncSession, link_id: int) -> int:
    result = await db.execute(
        select(func.count()).select_from(ClickEvent).where(ClickEvent.link_id == link_id)
    )
    return result.scalar_one()