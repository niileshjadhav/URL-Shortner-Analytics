import redis.asyncio as redis
from app.config import settings

redis_client = redis.from_url(settings.REDIS_URL, decode_responses = True)

async def get_cache(key:str):
    return await redis_client.get(key)


async def set_cache(key:str, value: str, ttl: int = 300):
    await redis_client.set(key, value, ex=ttl)


async def delete_cache(key:str):
    await redis_client.delete(key)



