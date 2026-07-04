from app.api.services.cache import redis_client

async def is_allowed(ip:str, limit:int = 10, window:int = 60):

    key = f"rate_limit:{ip}"

    current = await redis_client.get(key)

    if current and int(current) >= limit:
        return False
    
    pipe = redis_client.pipeline()
    pipe.incr(key, 1)
    pipe.expire(key, window)
    await pipe.execute()
    
    return True