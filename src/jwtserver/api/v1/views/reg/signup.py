from aioredis import Redis
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette.status import HTTP_201_CREATED

from jwtserver.api.v1.help_func.ParseToken import TokenProcessor
from jwtserver.models import User
from jwtserver.app import app
from fastapi import Depends, Response
from jwtserver.functions.init_redis import redis_conn
from jwtserver.functions.secure import get_password_hash
from jwtserver.functions.session_db import async_db_session
from jwtserver.functions.config import load_config

config = load_config().token


class Data(BaseModel):
    telephone: str
    password: str
    reg_token: str


class AccessTokenResponseModel(BaseModel):
    access_token: str
    token_type: str


# @app.post("/api/v1/auth/reg_user", response_model=schemas.TokenPD, status_code=HTTP_201_CREATED)
@app.post("/api/v1/signup/",
          tags=["Registration"],
          response_model=AccessTokenResponseModel,
          description="Registration user by login and password",
          status_code=HTTP_201_CREATED)
async def reg_user(
        response: Response,
        data: Data = None,
        # form_data: RegRequestForm = Depends(),
        redis: Redis = Depends(redis_conn),
        session: AsyncSession = Depends(async_db_session)
):
    if not await redis.get(f"{data.telephone}_reg_token"):
        return {"error": "bad reg token"}
    else:
        stmt = select(User).where(User.telephone == data.telephone)
        if (await session.execute(stmt)).scalars().first():
            return {"error": "user exist"}
        else:
            hashed_password = get_password_hash(data.password)
            new_user = User(telephone=data.telephone, is_active=True, password=hashed_password)
            session.add(new_user)
            await session.commit()
            token_processor = TokenProcessor()
            access_token, refresh_token = token_processor.create_pair_tokens(new_user.uuid.hex)

            await redis.delete(data.telephone)
            await redis.delete(f"{data.telephone}_reg_token")

            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=True,
                max_age=config.refresh_expire_time * 60)
            return {"access_token": access_token, "token_type": "JSv1"}
