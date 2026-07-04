from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.cache import get_cache, set_cache
from app.services.link_service import get_link
from app.services.analytics import record_click
from datetime import datetime, UTC


router = APIRouter(tags=["Redirect"])


@router.get("/{code}")
async def redirect(code: str, request: Request, db: AsyncSession = Depends(get_db)):

    cache_key = f"link:{code}"
    cached_url = await get_cache(cache_key)

    # CACHE HIT
    if cached_url:
        if not cached_url.get("is_active"):
            raise HTTPException(status_code=410, detail="Link is no longer active")

        expires_at_str = cached_url.get("expires_at")
        if expires_at_str:
            expires_at = datetime.fromisoformat(expires_at_str)
            if expires_at < datetime.now(UTC):
                raise HTTPException(status_code=410, detail="Link has expired")

        ip = request.client.host if request.client else None
        referrer = request.headers.get("referer")

        await record_click(db, link_id=cached_url["id"], ip=ip, referrer=referrer)

        return RedirectResponse(url=cached_url["target_url"])


    # CACHE MISS
    link = await get_link(db, code)

    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    if not link.is_active:
        raise HTTPException(status_code=410, detail="Link is no longer active")

    if link.expires_at and link.expires_at < datetime.now(UTC):
        raise HTTPException(status_code=410, detail="Link has expired")

    # Compute TTL: respect link expiry, cap at 600s
    ttl = 600
    if link.expires_at:
        remaining = int((link.expires_at - datetime.now(UTC)).total_seconds())
        ttl = max(1, min(ttl, remaining))

    await set_cache(
        cache_key,
        {
            "id": link.id,
            "target_url": link.target_url,
            "is_active": link.is_active,
            "expires_at": link.expires_at.isoformat() if link.expires_at else None,
        },
        ttl=ttl
    )

    ip = request.client.host if request.client else None
    referrer = request.headers.get("referer")

    await record_click(db, link_id=link.id, ip=ip, referrer=referrer)

    return RedirectResponse(url=link.target_url)
