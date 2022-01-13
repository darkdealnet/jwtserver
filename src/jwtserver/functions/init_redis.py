import aioredis
from jwtserver.functions.config import load_config

config = load_config().redis

# pool = aioredis.ConnectionPool.from_url(
#     config.url, max_connections=config.max_connections
# )
# redis = aioredis.Redis(connection_pool=pool)
redis = aioredis.from_url(config.url, decode_responses=True)


# async def redis_conn():
#     """Redis pool fabric connection, auto close connection"""
#     async with redis.client() as conn:
#         yield conn

def redis_conn():
    try:
        r = redis.client()
        yield r
    finally:
        r.close()
