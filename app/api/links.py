from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.link import LinkCreate, LinkResponse
from app.services.link_service import create_link, get_link


router = APIRouter(prefix="/links", tags=["Links"])

@router.post("/", response_model=LinkResponse)
async def create_short_link(payload:LinkCreate, db:AsyncSession = Depends(get_db)):

    custom_code = payload.custom_code or None

    if custom_code:
        existing_link = await get_link(db, custom_code)
        if existing_link:
            raise HTTPException(status_code=400, detail="Custom code already exists")

    try:
        link = await create_link(db, str(payload.target_url), custom_code)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    return link

@router.get("/{code}", response_model=LinkResponse)
async def get_short_link(code:str, db:AsyncSession = Depends(get_db)):

    link = await get_link(db, code)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    
    return link