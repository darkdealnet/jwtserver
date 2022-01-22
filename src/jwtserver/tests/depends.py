import aioredis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from jwtserver import models
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

sync_engine = create_engine(
    "postgresql://jwtserver:jwtserver-password@localhost:5433/jwtserver-tests")
async_engine = create_async_engine(
    "postgresql+asyncpg://jwtserver:jwtserver-password@localhost:5433/jwtserver-tests")
TestingSessionLocal = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)
# redis = aioredis.from_url("redis://:@localhost:6380/1", decode_responses=True)

pool = aioredis.ConnectionPool.from_url(
    "redis://:@localhost:6380/1", max_connections=10, decode_responses=True)
redis = aioredis.Redis(connection_pool=pool)

models.Base.metadata.drop_all(bind=sync_engine)
models.Base.metadata.create_all(bind=sync_engine)


def override_redis_client():
    return redis.client()


def override_async_db_session():
    """Databases pool fabric connection, auto close connection"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def override_redis_conn():
    try:
        r = redis.client()
        yield r
    finally:
        r.close()
