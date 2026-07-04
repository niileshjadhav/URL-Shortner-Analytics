import uvicorn
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from fastapi import FastAPI, Depends, Request
from app.api.db.session import get_db
from app.api.services.rate_limiter import is_allowed
from app.api.v1 import links, redirect, analytics


app = FastAPI(title="URL Shortner Service")

app.include_router(links.router, prefix="/api/v1")
app.include_router(redirect.router)
app.include_router(analytics.router, prefix="/api/v1")


@app.get("/", tags=["Test Me"])
async def health():
    return {"status": "Running Me!"}


@app.get("/db-test", tags=["Test Me"])
async def db_test(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT 1"))
    return {
        "database": "connected",
        "result" : result.scalar()
    }


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):

    ip = request.client.host if request.client else "unknown"

    allowed = await is_allowed(ip)

    if not allowed:
        return JSONResponse(
            status_code=429,
            content={"message": "Rate limit exceeded. Please try again later."}
        )
    
    return await call_next(request)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8006)
    print("Server started at http://localhost:8006")
    