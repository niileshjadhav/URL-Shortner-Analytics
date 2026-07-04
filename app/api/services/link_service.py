from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.models.link import Link
from app.api.services.shortener import generate_code

async def create_link(db: AsyncSession, target_url: str, custom_code:str|None = None):
    
    code = custom_code or generate_code()

    # Collision check
    existing = await db.execute(select(Link).where(Link.code == code))
    existing_link = existing.scalar_one_or_none()

    if existing_link:
        raise ValueError("Code already exists")
    
    link = Link(code=code, 
                target_url=target_url,  
                expires_at=datetime.now(UTC) + timedelta(seconds=30)
                )
    db.add(link)
    await db.commit()
    await db.refresh(link)

    return link


async def get_link(db:AsyncSession, code:str):
    result = await db.execute(select(Link).where(Link.code == code))
    link = result.scalar_one_or_none()
    return link

