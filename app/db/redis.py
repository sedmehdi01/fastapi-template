import redis.asyncio as aioredis
from redis.asyncio import Redis
from config import settings


async def get_redis_client() -> Redis:
    redis = await aioredis.from_url(
        settings.REDIS_URI,
        max_connections=10,
        encoding="utf8",
        decode_responses=True,
    )
    return redis
