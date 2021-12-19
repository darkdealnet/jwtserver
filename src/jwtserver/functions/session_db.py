from jwtserver.database import (
    AsyncSessionLocal,
)
from sqlalchemy.ext.asyncio import AsyncSession


async def async_db_session() -> AsyncSession:
    """Databases pool fabric connection, auto close connection"""
    async with AsyncSessionLocal() as session:
        yield session
