import redis.asyncio as redis

from src.config import Config

redis_url = Config.REDIS_URL

redis_pool = redis.ConnectionPool.from_url(
    redis_url,
    decode_responses=True,
    max_connections=50
)

async def get_redis() -> redis.Redis:
    return redis.Redis(connection_pool=redis_pool)