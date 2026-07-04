import redis.asyncio as redis
from app.config import settings
import json

redis_client = redis.from_url(settings.REDIS_URL, decode_responses = True)


async def get_cache(key: str):
    value = await redis_client.get(key)
    if value is None:
        return None
    return json.loads(value)


async def set_cache(key: str, value, ttl: int = 600):
    if isinstance(value, (dict, list)):
        value = json.dumps(value)

    await redis_client.set(key, value, ex=ttl)


async def delete_cache(key: str):
    await redis_client.delete(key)



