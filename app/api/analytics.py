from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.analytics import get_total_clicks
from app.services.link_service import get_link

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/{code}/clicks")
async def get_clicks(code: str, db: AsyncSession = Depends(get_db)):

    link = await get_link(db, code)

    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    
    clicks = await get_total_clicks(db, link.id)

    return {
        "code": code,
        "total_clicks": clicks
    }