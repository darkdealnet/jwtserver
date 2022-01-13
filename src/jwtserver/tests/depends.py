import aioredis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from jwtserver import models
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from jwtserver.Google.Recaptcha_v3 import Recaptcha

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"
sync_engine = create_engine(
    "postgresql://jwtserver:jwtserver-password@localhost:5433/jwtserver-tests")
async_engine = create_async_engine(
    "postgresql+asyncpg://jwtserver:jwtserver-password@localhost:5433/jwtserver-tests")
TestingSessionLocal = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)
redis = aioredis.from_url("redis://:@localhost:6380/1", decode_responses=True)

models.Base.metadata.drop_all(bind=sync_engine)
models.Base.metadata.create_all(bind=sync_engine)


# async def override_async_db_session():
#     """Databases pool fabric connection, auto close connection"""
#     async with TestingSessionLocal() as session:
#         yield session


def override_async_db_session():
    """Databases pool fabric connection, auto close connection"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# async def override_redis_conn():
#     """Redis pool fabric connection, auto close connection"""
#     async with redis.client() as conn:
#         yield conn

def override_redis_conn():
    try:
        r = redis.client()
        yield r
    finally:
        r.close()


class OverrideRecaptcha(Recaptcha):
    async def check(self) -> 'Recaptcha':
        # self.r_json = tokens[self.recaptcha_token.split(":")]
        self.r_json = {
            "success": self.recaptcha_token.split(":")[0],
            "action": self.recaptcha_token.split(":")[1],
            "score": float(self.recaptcha_token.split(":")[2]),
        }
        return self
