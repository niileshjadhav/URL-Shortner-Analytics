from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.db.session import get_db
from app.api.services.cache import get_cache, set_cache
from app.api.services.link_service import get_link
from app.api.services.analytics import record_click


router = APIRouter(tags=["Redirect"])


@router.get("/{code}")
async def redirect(code: str, request: Request, db: AsyncSession = Depends(get_db)):
    
    cache_key = f"link:{code}"

    cached_url = await get_cache(cache_key)
    if cached_url:
        return RedirectResponse(url=cached_url)
    
    link = await get_link(db, code)

    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    if not link.is_active:
        raise HTTPException(status_code=410, detail="Link is no longer active")

    from datetime import datetime, UTC
    if link.expires_at and link.expires_at < datetime.now(UTC):
        raise HTTPException(status_code=410, detail="Link has expired")

    await set_cache(cache_key, link.target_url, ttl=600)

    ip = request.client.host if request.client else None
    referrer = request.headers.get("referer")
    await record_click(db, link_id=link.id, ip=ip, referrer=referrer)

    return RedirectResponse(url=link.target_url)
