from typing import Optional

import aioredis.exceptions
from aioredis import Redis
from fastapi import Depends, Body
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from jwtserver.Google.Recaptcha_v3 import Recaptcha
from jwtserver.functions.init_redis import redis_conn
from jwtserver.models import User
from jwtserver.app import app
from pydantic import BaseModel
from jwtserver.functions.session_db import async_db_session


class Data(BaseModel):
    telephone: str


class ResponseModel(BaseModel):
    free: bool
    telephone: str
    sent: Optional[bool]
    time: Optional[int]


@app.post("/api/v1/auth/phone_status/", response_model=ResponseModel, tags=["Registration"])
async def phone_status(
        telephone: str = Body(...),
        redis: Redis = Depends(redis_conn),
        session: AsyncSession = Depends(async_db_session),
        recaptcha: Recaptcha = Depends(Recaptcha)
):
    await recaptcha.set_action_name('SignUpPage/PhoneStatus').greenlight()
    stmt = select(User).where(User.telephone == telephone)
    result = await session.execute(stmt)
    if result.scalars().first():
        return {"free": False, "telephone": telephone}
    try:
        code_is_send = await redis.get(telephone)
    except aioredis.exceptions.ConnectionError:
        logger.info('Redis ConnectionError')
        code_is_send = None

    if code_is_send:
        ttl = await redis.ttl(telephone)
        return {"free": True, "telephone": telephone, "sent": True, "time": ttl}
    return {"free": True, "telephone": telephone}
