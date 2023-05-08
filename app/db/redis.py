from redis.asyncio import Redis
from config import settings

redis_db: Redis = Redis.from_url(settings.REDIS_URI, decode_responses=True)
