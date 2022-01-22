import aioredis
# from fastapi import Depends

# from jwtserver.app import get_config
from jwtserver import settings

settings = settings.get_settings()


# def create_pool_redis(config: ConfigModel = Depends()):
def create_pool_redis():
    pool = aioredis.ConnectionPool.from_url(
        settings.redis.redis_dsn,
        max_connections=settings.redis.max_connections,
        decode_responses=True,
    )
    redis = aioredis.Redis(connection_pool=pool)
    return redis


async def redis_conn():
    r = create_pool_redis().client()
    try:
        yield r
    finally:
        await r.close()
